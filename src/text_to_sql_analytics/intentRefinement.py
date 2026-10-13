import logging
import os, sys
from llm_initialzation import create_llm, call_llm_string_response
from utils import setup_logger, load_configurations

# Configure logging for error visibility
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     handlers=[
#         logging.FileHandler("intent.logs", mode='a'), # Saves to the exact same file
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# logger = logging.getLogger(__name__)
logger = setup_logger("IntentRefinement", "refinement.logs")

llm = None

def init_refinement_llm():
    """Waits to initialize the LLM until after .cfg files are loaded."""
    global llm
    if llm is None:
        try:
            logger.info("Initializing Refinement LLM...")
            llm = create_llm(custom_logger=logger)
        except Exception:
            logger.exception('Failed to initialize LLM')
            sys.exit(1)

LIST_OF_AGENT_TASKS = [
    "Retrieve most failed test cases for the current user",
    "Identify modules or components of the application that fail the most (Web, API, PDF)",
    "Get summary of latest or selected test run (pass, fail, skip, success rate)",
    "Retrieve execution history of test cases",
    "Analyze failure trends over time",
    "Extract top failure reasons and error messages",
    "Identify flaky or unstable test cases",
    "Compare test results across runs, builds, or time ranges",
    "Retrieve user-specific test execution insights and metrics",
    "Filter and retrieve test cases by status, date range, module, environment, or application type (Web, API, PDF)",
    "Identify failing API endpoints, web pages, UI elements, or PDF validations",
    "Get performance insights such as slowest or long-running test cases",
    "Generate high-level test execution and failure analysis summaries",
    "Answer natural language queries about executed test cases and testing insights for the current user"
]

def _call_refiner_llm(intent_list: list) -> str:
    """
    Takes a single, focused list of context and compresses it into one perfect sentence.
    """
    global llm
    if llm is None:
        init_refinement_llm()
        
    try:
        formatted_context = "\n".join([f"- {item}" for item in intent_list])

        system_prompt = f"""You are an Intent Refiner for a Testing Analytics Agent.
Your job is to read the provided user context and summarize their request into ONE perfect, highly specific sentence.

You must map their request to the core goal of one of these supported tasks:
{', '.join(LIST_OF_AGENT_TASKS)}

Strict Rules:
1. PRESERVE EXPLICIT FILTERS (CRITICAL): If the user asks for a specific status (e.g., "failed", "passed"), a specific timeframe (e.g., "latest baseline"), or specific metrics, you MUST explicitly include those exact filters in your refined sentence. DO NOT generalize to a full summary (pass/fail/skip) if they only asked for failures.
2. INCLUDE CONTEXT: You MUST include the specific Workspace(s) and Testing Type(s) in your final sentence.
3. FORMAT: Output ONLY the refined sentence. Do not include introductory text like "The user wants...".
4. CRITICAL OUTPUT FORMAT:
        You MUST output a valid JSON dictionary where EVERY relevant testing domain gets its own separate key. NEVER group multiple domains into a single key.

        BAD OUTPUT:
        {{ "web, api, package": "Retrieve failed test cases..." }}

        GOOD OUTPUT:
        {{
            "web": "Retrieve failed test cases for WEB testing.",
            "api": "Retrieve failed test cases for API testing.",
            "package": "Retrieve failed test cases for PACKAGE testing."
        }}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the collected context and conversation:\n\n{formatted_context}\n\nPlease generate the refined, single-sentence query."}
        ]

        refined_query = call_llm_string_response(messages, llm,custom_logger=logger)
        return refined_query

    except Exception:
        logger.exception('Error during intent refinement')
        return 'Error in intent refinement'

def intent_refinement(intent_list: list) -> dict:
    """
    Parses the intent_list. Dynamically counts how many domains are present 
    based on commas, and calls the worker exactly that many times.
    """
    # 1. Find and extract just the domain names from the list
    testing_types_str = ""
    for item in intent_list:
        if "Testing Types:" in item:
            # Strip out the label, leaving just "WEB, API, PACKAGE"
            testing_types_str = item.replace("Testing Types:", "").strip()
            break

    results = {}
    
    # 2. Split the string by commas into a neat Python list
    # Handles "All Domains" edge case just in case the UI ever passes it!
    if "All Domains" in testing_types_str:
        domains_to_process = ["WEB", "API", "PDF", "PACKAGE"]
    else:
        # Splits "WEB, API" into ['WEB', 'API']
        domains_to_process = [d.strip() for d in testing_types_str.split(",") if d.strip()]
        
    # 3. Accurate Logging
    if len(domains_to_process) > 1:
        logger.info(f"Smart Router: Detected {len(domains_to_process)} domains. Splitting calls.")
    else:
        logger.info("Smart Router: Single domain detected.")

    # 4. Loop through however many domains were found
    for domain in domains_to_process:
        # Build a temporary list specifically for this single domain
        domain_list = []
        for item in intent_list:
            if "Testing Types:" in item:
                domain_list.append(f"Testing Types: {domain}")
            else:
                domain_list.append(item)
                
        # Call the LLM worker and save it to the dictionary
        results[domain.lower()] = _call_refiner_llm(domain_list)

    return results

if __name__ == "__main__":
    import argparse
    import configparser
    import sys

    # 1. Catch the .cfg files from the command line
    parser = argparse.ArgumentParser(description="Run Intent Refinement")
    parser.add_argument('--tool-config', required=True)
    parser.add_argument('--keys-config', required=True)
    args = parser.parse_args()

    try:
        load_configurations(args.tool_config, args.keys_config)
    except Exception as e:
        logger.error(f"Failed to load configurations: {e}")
        raise
    # # 2. Read the files and load keys into memory
    # config = configparser.ConfigParser()
    # if not config.read([args.tool_config, args.keys_config]):
    #     print("ERROR: Could not read configuration files.")
    #     sys.exit(1)

    # for section in config.sections():
    #     for key, value in config.items(section):
    #         os.environ[key.upper()] = value

    # 3. Test the code with the exact list output you got from the Validator!
    mock_intent_list = ['Workspaces: Mounikalocal', 'Testing Types: All Domains (WEB, API, PDF, PACKAGE)', 'User Query: give a report of failed testcases in latest baseline']
    refined_query = intent_refinement(mock_intent_list)

    print(refined_query)