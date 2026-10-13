import json
import argparse
from utils import setup_logger, load_configurations
from llm_initialzation import create_llm, call_llm_string_response
from global_vars import (
    is_web_selected,
    is_api_selected,
    is_pdf_selected,
    is_package_selected,
    web_user_intent,
    api_user_intent,
    pdf_user_intent,
    package_user_intent,
    web_json,
    api_json,
    pdf_json,
    package_json
)


# Logger
logger = setup_logger("processUserQuery", "processUserQuery.logs")

# Utility
def call_llm_with_logging(messages, llm, step):
    
    for msg in messages:
        logger.info("LLM PROMPT [%s][%s]:\n%s", step, msg["role"], msg["content"])

    response = call_llm_string_response(messages, llm)
    logger.info("LLM RESPONSE [%s]: %s", step, response)
    return response.strip()

def clean_llm_json_response(response: str) -> str:
    """
    Removes markdown code fences from LLM responses.
    """
    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    return response

# JSON Reader
def read_data_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f).get("data", [])

def derive_columns_from_data(data):
    return list(data[0].keys()) if data else []

# STEP 1: DOMAIN IDENTIFICATION FROM BOOLEANS
def identify_domains_from_booleans():
    domain_flags = {
        "web": is_web_selected,
        "api": is_api_selected,
        "pdf": is_pdf_selected,
        "package": is_package_selected
    }

    selected_domains = [
        domain for domain, enabled in domain_flags.items() if enabled
    ]

    logger.info(
        "STEP_1_IDENTIFY_DOMAIN: Selected domains = %s",
        selected_domains
    )

    return selected_domains


# STEP 2: IDENTIFY END GOAL (SEMANTIC)
def identify_end_goal(user_query, llm):
    prompt = (
        f"""
            User Intent:
            {user_query}

            Task:
            By analysing user intent, determine what the user wants to know.

            Rules:
            - Identify the user's intent or end goal
            - Use a short, clear phrase or category
            - Do NOT include explanations or multiple options
            - Return ONLY the end goal
        """

    )

    response = call_llm_with_logging(
        [{"role": "user", "content": prompt}],
        llm,
        "STEP_2_END_GOAL"
    )

    return response if response else "OTHER"


# STEP 3: DATA AVAILABILITY CHECK
def check_data_availability(end_goal, dataset_columns, llm):
    prompt = (
        f"""
            End goal: {end_goal}

            Dataset columns:{dataset_columns}

            Question:
            Does the dataset contain a column that can represent the end goal?
            Does the dataset contain AT LEAST ONE column that helps address the end goal?
            Return ONLY yes or no.
        """
        # Does the dataset contain AT LEAST ONE column that helps address the end goal?
    )

    response = call_llm_with_logging(
        [{"role": "user", "content": prompt}],
        llm,
        "STEP_3_DATA_AVAILABILITY"
    ).lower()

    return "yes" if response == "yes" else "no"


# STEP 4: COLUMN IDENTIFICATION
def identify_relevant_column(end_goal, dataset_columns, availability, llm):
    if availability == "no" or not dataset_columns:
        return []

    prompt = f"""
        End goal: {end_goal}

        Dataset columns:
        {dataset_columns}

        Rules:
        - Select ALL relevant column(s) that best satisfy the End goal
        - Choose ONLY from the provided dataset columns
        - Do NOT hallucinate new columns
        - Return the result STRICTLY as a JSON array of strings
    """

    # response = call_llm_with_logging(
    #     [{"role": "user", "content": prompt}],
    #     llm,
    #     "STEP_5_COLUMN_IDENTIFICATION"
    # )
    raw_response = call_llm_with_logging(
    [{"role": "user", "content": prompt}],
    llm,
    "STEP_4_COLUMN_IDENTIFICATION"
    )

    cleaned_response = clean_llm_json_response(raw_response)

    # -----------------------------
    # Safe JSON parsing + filtering
    # -----------------------------
    try:
        selected_columns = json.loads(cleaned_response)

        if not isinstance(selected_columns, list):
            return []

        valid_columns = [
            col for col in selected_columns if col in dataset_columns
        ]

        return valid_columns

    except json.JSONDecodeError as e:
        logger.error(
            "Invalid JSON after cleaning. Raw: %s | Cleaned: %s | Error: %s",
            raw_response,
            cleaned_response,
            str(e)
        )
        return []


# STEP 5: RESULT QUANTITY
def identify_result_quantity(query, llm):
    prompt = (
        f"""
            Query:
            {query}
           
            Task:
            Identify how many results the user wants.

            Rules:
            - Return ONLY one word
            - Allowed values:
            - single
            - multiple
            - unspecified
            - Do NOT add explanations or extra text
        """

    )

    response = call_llm_with_logging(
        [{"role": "user", "content": prompt}],
        llm,
        "STEP_5_RESULT_QUANTITY"
    ).lower()

    return response if response in {"single", "multiple", "unspecified"} else "unspecified"


# STEP 6: DOMAIN‑LEVEL FINAL ANSWER GENERATION
def generate_final_user_answer(
    user_query,
    end_goal,
    data_available,
    relevant_columns,
    result_quantity,
    data_rows,
    llm ):
    """
    Generates the final user-facing answer for a single domain
    ONLY if sufficient data is available.
    """

    if data_available != "yes" or not relevant_columns:
        return "Data insufficient to answer the query"

    available_data = data_rows

    prompt = f"""
        User query:
        {user_query}

        End goal:
        {end_goal}

        Relevant columns:
        {relevant_columns}

        Result quantity:
        {result_quantity}

        Available data:
        {available_data}

        Task:
        Identify which rows answer the user's query.

       Rules:
        - Use ONLY the dataset provided.
        - Do NOT rewrite or reformat any data.
        - Do NOT include any of the row contents in your reply.
        - Return ONLY a JSON array of run_id values where the row matches the user query.
        - If no rows match, return an empty JSON array.
        - Return ONLY valid JSON.
    """

    raw_response = call_llm_with_logging(
        [{"role": "user", "content": prompt}],
        llm,
        "STEP_6_FINAL_ANSWER"
    )
    
    cleaned = clean_llm_json_response(raw_response)


    try:
        matched_ids = json.loads(cleaned)
        if not isinstance(matched_ids, list):
            return "Data insufficient to answer the query"
    except json.JSONDecodeError:
        return "Data insufficient to answer the query"

    
    # Reconstruct full rows
    final_rows = []
    for row in data_rows:
        row_values = list(row.values())
        if any(matched_id in row_values for matched_id in matched_ids):
            final_rows.append(row)

    if not final_rows:
        return "Data insufficient to answer the query"

    if result_quantity == "single":
        return final_rows[0]

    return final_rows


# PROCESSOR
def process_single_domain(json_path, domain, user_query, llm):
    data = read_data_from_json(json_path)
    dataset_columns = derive_columns_from_data(data)

    end_goal = identify_end_goal(user_query, llm)
    availability = check_data_availability(end_goal, dataset_columns, llm)
    relevant_columns = identify_relevant_column(
        end_goal, dataset_columns, availability, llm
    )
    quantity = identify_result_quantity(user_query, llm)


    final_answer = generate_final_user_answer(
        user_query=user_query,
        end_goal=end_goal,
        data_available=availability,
        relevant_columns=relevant_columns,
        result_quantity=quantity,
        data_rows=data,
        llm=llm
    )

    return {
        "domain": domain,
        "user_query": user_query,
        "end_goal": end_goal,
        "data_available": availability,
        "relevant_columns": relevant_columns,
        "result_quantity": quantity,
        "dataset_columns": dataset_columns,
        "source_json": json_path,
        "final_answer": final_answer or "Data insufficient to answer the query"
    }


# ORCHESTRATOR
def process_all_domains(llm):
    results = []
    domains = identify_domains_from_booleans()

    domain_to_json = {
        "web": web_json,
        "api": api_json,
        "pdf": pdf_json,
        "package": package_json
    }

    domain_to_user_intent = {
        "web": web_user_intent,
        "api": api_user_intent,
        "pdf": pdf_user_intent,
        "package": package_user_intent,
    }

    for domain in domains:
        json_path = domain_to_json.get(domain)
        user_query = domain_to_user_intent.get(domain)
        if not json_path or not user_query:
            logger.warning("Skipping domain %s due to missing intent or data", domain)
            continue

        logger.info(
            "==================== START DOMAIN PROCESSING ====================\n"
            "Domain: %s\n"
            "Source JSON: %s\n"
            "=================================================================================================================",
            domain,
            json_path
        )

        
        domain_result = process_single_domain(
            json_path=json_path,
            domain=domain,
            user_query=user_query,
            llm=llm)

        results.append(domain_result)

        logger.info(
            "==================== END DOMAIN PROCESSING ====================\n"
        )

    return results


# ENTRY POINT
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-config", required=True)
    parser.add_argument("--keys-config", required=True)
    args = parser.parse_args()

    load_configurations(args.tool_config, args.keys_config)

    llm = create_llm()
    logger.info("LLM initialized")

    output = process_all_domains(llm)

    output_path = "output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    logger.info("Output written to %s", output_path)
    
    try:
        with open(output_path, "r", encoding="utf-8") as f:
            output_content = f.read()

        logger.info(
            "==================== OUTPUT.JSON CONTENT ====================\n"
            "%s\n"
            "================================================================",
            output_content
        )
    except Exception as e:
        logger.error("Failed to log output.json content: %s", str(e))

    print(f"Output written to {output_path}")