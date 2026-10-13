from llm_initialzation import create_llm, call_llm_string_response, call_llm_formatted_response
from utils import setup_logger, load_configurations
from databaseQueryExecutor import fetch_user_workspaces
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import os
import sys
import logging
import json
import time
import argparse
import configparser
import global_vars
# Configure logging for error visibility
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     handlers=[
#         logging.FileHandler("intent.logs", mode='a'), # Saves to file
#         logging.StreamHandler(sys.stdout)             # Keeps it visible in terminal
#     ]
# )
# logger = logging.getLogger(__name__)    
logger = setup_logger("IntentClassificationAndFilter","intent.logs")

LIST_OF_AGENT_TASKS = [
    "Retrieve most failed test cases for the current user",
    "Identify modules or components of the application that fail the most (Web, API, PDF, Package)",
    "Get summary of latest or selected test run (pass, fail, skip, success rate)",
    "Retrieve execution history of test cases",
    "Analyze failure trends over time",
    "Extract top failure reasons and error messages",
    "Identify flaky or unstable test cases",
    "Compare test results across runs, builds, or time ranges",
    "Retrieve user-specific test execution insights and metrics",
    "Filter and retrieve test cases by status, date range, module, environment, or application type (Web, API, PDF, Package)",
    "Identify failing API endpoints, web pages, UI elements, or PDF validations",
    "Get performance insights such as slowest or long-running test cases",
    "Generate high-level test execution and failure analysis summaries",
    "Answer natural language queries about executed test cases and testing insights for the current user"
]

# prompt1 = """You are an intent classifier for an AI agent.

# Your task is to determine whether the user’s query intends to perform ANY of the tasks supported by the agent (including closely related, similar, paraphrased, or implicitly stated tasks).

# Instructions:
# 1. Carefully analyze the user query.
# 2. Compare the intent with the agent’s supported tasks.
# 3. If the query clearly matches or implies a similar task → response = "Yes"
# 4. If the query is unrelated to all supported tasks → response = "No"
# 5. If the query is ambiguous, incomplete, or requires more details to determine intent → ask a single clarification question as the response.

# Confidence Definition:
# - Confidence represents how certain you are that your classification (Yes/No/Clarification question) is correct.
# - Use an integer from 0 to 100.
# - High confidence (80–100): Clear and explicit intent.
# - Medium confidence (50–79): Likely intent but some ambiguity.
# - Low confidence (1–49): Weak signals or unclear mapping.
# - If you ask a clarification question, confidence should reflect uncertainty (typically 0–40).

# Strict Output Rules:
# - Output ONLY valid JSON.
# - Do NOT include explanations, extra text, or markdown.
# - The JSON format must be exactly:
#   {\"response\": str, \"confidence\": int}
# - \"response\" must be either:
#   - \"Yes\"
#   - \"No\"
#   - A single clarification question
# - The clarification question must be concise and directly help disambiguate intent.
# - Consider synonyms, indirect phrasing, and semantically similar requests as valid matches.
# - If the query likely relates to a supported task but lacks sufficient detail, prefer asking a clarification question over responding \"No\".

# Agent Supported Tasks:
# {LIST_OF_AGENT_TASKS}

# User Query:
# {USER_QUERY}"""

# prompt2 = """You are an intent classifier for a Testing Analytics Agent.

# Agent Capability Scope:
# - The agent ONLY retrieves, analyzes, and summarizes information about already executed test cases for the current user from the database.
# - The agent DOES NOT generate code, scripts, automation logic, or perform new test execution.
# - The agent DOES NOT perform development tasks such as writing Python, SQL, or any programming code.
# - The agent ONLY handles insight extraction, analytics, filtering, comparison, and summaries of existing test execution data (Web, API, PDF testing).

# Your task is to determine whether the user’s query intends to perform ANY supported analytics or data-extraction task.

# Critical Classification Rule:
# - If the user asks to write code, scripts, functions, pipelines, or implementation (even if related to testing analytics), the response MUST be \"No\".
# - Example: “Write python code to analyze failure trends” → No (out of scope)

# Instructions:
# 1. Analyze the user query intent.
# 2. Match it strictly against the agent’s capability scope.
# 3. If the query is about extracting, analyzing, summarizing, filtering, or retrieving executed test case insights → \"Yes\"
# 4. If the query asks for code generation, system design, automation creation, or any development task → \"No\"
# 5. If the intent is unclear but likely related to test execution insights → ask a single clarification question.

# Confidence Definition:
# - Confidence (0–100) represents how certain you are that the classification is correct.

# Strict Output Rules:
# - Output ONLY valid JSON.
# - No explanations, no extra text.
# - Format must be exactly:
#   {\"response\": str, \"confidence\": int}
# - \"response\" must be:
#   - \"Yes\"
#   - \"No\"
#   - A single clarification question

# Agent Supported Tasks:
# {LIST_OF_AGENT_TASKS}

# User Query:
# {USER_QUERY}"""

prompt = """You are the Intent Validator for a Testing Analytics Agent.

Agent Capability Scope:
- The agent ONLY retrieves, filters, analyzes, and summarizes information about already executed test cases for the current user from the database.
- Supported domains: Web testing, API testing, and PDF testing.
- The agent DOES NOT generate code, scripts, automation logic, or run new tests.
- The agent DOES NOT perform development tasks (e.g., writing Python, SQL, or pipelines).
- The agent ONLY answers queries related to executed test case data and testing analytics.

You must evaluate the user's intent by analyzing the ENTIRE conversation history. Combine the user's initial request with any follow-up clarifications they have provided. Use this combined context to perform a strict 2-Step Validation Process:

=== STEP 1: SCOPE VALIDATION (Gatekeeper) ===
First, determine if the combined query is legally allowed to be processed.
1. If the query asks to write code, scripts, functions, or implementation → response = \"No\"
2. If the query is entirely unrelated to test execution data or analytics → response = \"No\"
If the query fails Step 1, STOP HERE and output \"No\". Do not proceed to Step 2.

=== STEP 2: DATA SUFFICIENCY CHECK ===
If the query passes Step 1, check if you have enough data to generate a SQL query.
Look for THREE mandatory filters in the combined conversation history:
  a) TESTING DOMAIN: The user DOES NOT need to specify a testing domain (Web, API, PDF, Package). If they do not mention a domain, DO NOT ask them for it. Assume they want a cross-domain report across all systems. Consider the data SUFFICIENT and return "Yes".
  b) Timeframe (e.g., latest run, last 7 days, specific run, date range)
  c) Workspace / App Name (Must be valid options available to this user: {USER_WORKSPACES} - can be multiple)

- If ALL THREE filters are present (or strongly implied) in the chat history → response = "Yes"
- If ANY filter is missing → You MUST ask a single, concise clarification question requesting the missing information.
  - Example: "Show failed testcases" → Ask: "For which workspace, testing type (Web/API/PDF/Package), and timeframe?"
  - Example: "Show Web failures for last 7 days" → Ask: "Which workspace would you like to check? Your options are: {USER_WORKSPACES}"

Confidence Definition:
- Confidence (0–100) measures data sufficiency and certainty.
- 80–100: Scope is valid and data is fully sufficient (Yes) OR scope is explicitly forbidden (No).
- 1–79: Scope is valid, but data is insufficient (Clarification required).

Strict Output Rules:
- Output ONLY valid JSON. No markdown, no extra text.
- Output format MUST be exactly:
  {\"response\": str, \"confidence\": int}
- \"response\" must be either: \"Yes\", \"No\", or the clarification question."""

@dataclass
class AgentState:
    response: Optional[Any] = None
    confidence: int = 0
    history: List[Dict] = None
    timestamp: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)

# Set environment and initialize LLM with guarded error handling
# try:
#     os.environ['DEPLOYMENT_ENV'] = 'local'
#     os.environ['GPT_MODEL_NAME'] = MODEL_NAME
#     os.environ['GPT_LLM_API_KEY'] = API_KEY
#     os.environ['GPT_LLM_API_VERSION'] = API_VERSION
#     os.environ['GPT_LLM_ENDPOINTS'] = AZURE_ENDPOINTS
# except Exception:
#     logger.exception('Failed to set environment variables')
#     sys.exit(1)
llm = None
def init_intent_llm():
    global llm
    if llm is None:
        try:
            logger.info("Initializing Intent Validator LLM...")
            llm = create_llm(custom_logger=logger)
        except Exception:
            logger.exception('Failed to initialize LLM')
            sys.exit(1)

def filter_testing_types(user_query: str) -> list:
    """Extracts domains from the query."""
    types = []
    query_lower = user_query.lower()
    
    if "web" in query_lower: types.append("web")
    if "api" in query_lower: types.append("api")
    if "pdf" in query_lower: types.append("pdf")
    if "package" in query_lower: types.append("package")

    if not types:
        return ["web", "api", "pdf", "package"]
        
    return types

def set_testing_type_globals(selected_types: list):
    """Updates the variables in global_vars.py"""
    selected_lower = [t.lower().strip() for t in selected_types]
    
    # Because filter_testing_types now returns all 4 if missing, 
    # this logic works perfectly without needing to be changed!
    global_vars.is_web_selected = "web" in selected_lower
    global_vars.is_api_selected = "api" in selected_lower
    global_vars.is_pdf_selected = "pdf" in selected_lower
    global_vars.is_package_selected = "package" in selected_lower
    
    logger.info(f"Globals Set -> Web: {global_vars.is_web_selected}, API: {global_vars.is_api_selected}, PDF: {global_vars.is_pdf_selected}, Package: {global_vars.is_package_selected}")

def get_menu_selection(title: str, options: list) -> list:
    """Displays a numbered menu and allows multi-selection via comma-separated numbers."""
    print(f"\n=== {title} ===")
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
        
    while True:
        user_input = input(f"Select numbers (e.g., '1' or '1,3') (or 'exit'): ")
        if user_input.lower() == 'exit':
            return ['exit']
            
        try:
            # Parse the comma-separated string into a list of integers
            choices = [int(x.strip()) for x in user_input.split(',')]
            selected = []
            is_valid = True
            
            for choice in choices:
                if 1 <= choice <= len(options):
                    selected.append(options[choice - 1])
                else:
                    print(f"Error: '{choice}' is not a valid option.")
                    is_valid = False
                    break
                    
            if is_valid and selected:
                return selected
                
        except ValueError:
            print("Error: Invalid format. Use numbers separated by commas (e.g., 1, 2).")

def validate_user_intent(query: str, available_workspaces: list, history: Optional[List[Dict]] = None) -> Dict:
    """
    Run the intent validation for a single query and return an AgentState dict.
    Designed to be called from an orchestrator (e.g., LangGraph).
    """
    global llm 
    if llm is None:  
        init_intent_llm()

    # 1. Only inject the System Prompt on the very first turn!
    if history is None or len(history) == 0:
        # Format the workspaces into a readable string
        workspace_string = ", ".join(available_workspaces) if available_workspaces else "None Found"
        
        # Inject BOTH the tasks and the user's specific workspaces into the prompt
        system_content = prompt.replace(
            "{LIST_OF_AGENT_TASKS}", "\n- ".join(LIST_OF_AGENT_TASKS)
        ).replace(
            "{USER_WORKSPACES}", workspace_string
        )
        history = [{"role": "system", "content": system_content}]

    # 2. Append the new user message normally
    history.append({"role": "user", "content": query})

    try:
        response = call_llm_formatted_response(history, llm,custom_logger=logger)
    except Exception:
        logger.exception("LLM call failed in validate_user_intent")
        state = AgentState(response=None, confidence=0, history=history, timestamp=time.time())
        return state.to_dict()

    assistant_content = response.get("response") if isinstance(response, dict) else str(response)
    
    # 3. Append the LLM's response to keep the memory flowing
    history.append({"role": "assistant", "content": assistant_content})

    resp_value = None
    conf_value = 0

    if isinstance(response, dict) and "response" in response and "confidence" in response:
        resp_value = response.get("response")
        conf_value = int(response.get("confidence", 0))
    else:
        try:
            parsed = json.loads(assistant_content)
            resp_value = parsed.get("response")
            conf_value = int(parsed.get("confidence", 0)) if parsed.get("confidence") is not None else 0
        except Exception:
            resp_value = assistant_content
            conf_value = 0
    
    state = AgentState(response=resp_value, confidence=conf_value, history=history, timestamp=time.time())
    return state.to_dict()


def interactive_validation_loop() -> tuple:
    history = []
    
    # --- 1. SIMULATE AUTHENTICATION ---
    current_userid = input("Please enter your User ID (e.g., 43920821): ")
    
    # --- 2. CAPTURE USER INTENT FIRST ---
    print("\n" + "="*50)
    user_query = input("Enter your testing analytics query (e.g., 'give me failed screens'): ")
    if user_query.lower() == 'exit': return {}, history, []

    # --- 3. FETCH & SELECT WORKSPACES ---
    from databaseQueryExecutor import fetch_user_workspaces
    user_workspaces = fetch_user_workspaces(current_userid)
    
    if not user_workspaces:
        print("System Error: No workspaces found for this user. Cannot proceed.")
        return {}, history, []

    selected_workspaces = get_menu_selection("SELECT WORKSPACE(S)", user_workspaces)
    if 'exit' in selected_workspaces: return {}, history, []
    
    workspace_str = ", ".join(selected_workspaces)

    # --- 4. DYNAMICALLY FILTER & SELECT TESTING TYPES ---
    filtered_types = filter_testing_types(user_query) # This correctly returns all 4 if empty now!
    
    if global_vars.REQUIRE_DOMAIN_MENU:
        selected_testing_types = get_menu_selection("SELECT TESTING TYPE(S)", filtered_types)
        if 'exit' in selected_testing_types: return {}, history, []
        testing_str = ", ".join(selected_testing_types)
    else:
        # Silently adopt whatever the filter returned
        selected_testing_types = filtered_types 
        testing_str = "All Domains (WEB, API, PDF, PACKAGE)"

    # CRITICAL: Don't forget to actually call your setter function to update the globals!
    set_testing_type_globals(selected_testing_types)

    # --- 5. START AGENT VALIDATION LOOP ---
    print("\nSystem: Context gathered. Validating intent...")
    
    enriched_query = (
        f"User Query: {user_query}\n\n"
        f"[CRITICAL SYSTEM NOTE: The user has already explicitly selected "
        f"Workspace(s): '{workspace_str}' and Testing Type(s): '{testing_str}' "
        f"through the UI menus. You MUST consider these two data parameters "
        f"FULLY SATISFIED. DO NOT ask the user to provide them again.]"
    )
    
    current_agent_query = enriched_query

    while True:
        try:
            result_state = validate_user_intent(current_agent_query, user_workspaces, history=history)
        except Exception:
            logger.exception("Unexpected error while validating intent")
            break

        llm_response = result_state.get('response')
        history = result_state.get('history', history)

        if llm_response in ["Yes", "No"]:
            # Build the clean list
            clean_list = [
                f"Workspaces: {workspace_str}",
                f"Testing Types: {testing_str}"
            ]
            
            for msg in history:
                if msg.get('role') == 'user':
                    content = msg.get('content', '')
                    if "[CRITICAL SYSTEM NOTE:" in content:
                        clean_query = content.split('\n\n[CRITICAL SYSTEM NOTE:')[0]
                        clean_list.append(clean_query.strip())
                    else:
                        clean_list.append(content.strip())

            # Save core variables to the dictionary
            result_state['userid'] = current_userid
            result_state['workspace'] = selected_workspaces
            result_state['testing_type'] = selected_testing_types
            
            # Return THREE separate items!
            return result_state, history, clean_list
            
        else:
            user_reply = input(f"\nAgent asks: {llm_response}\nYour reply (or 'exit'): ")
            if user_reply.lower() == 'exit': return {}, history, []
            current_agent_query = user_reply

    return {}, history, []

if __name__ == "__main__":    
    # 1. Catch the .cfg files from the command line
    parser = argparse.ArgumentParser(description="Run Intent Validator")
    parser.add_argument('--tool-config', required=True, help="Path to tool configurations")
    parser.add_argument('--keys-config', required=True, help="Path to keys configurations")
    args = parser.parse_args()
    try:
        load_configurations(args.tool_config, args.keys_config)
    except Exception as e:
        logger.error(f"Failed to load configurations: {e}")
        raise

    # # 2. Read the .cfg files
    # config = configparser.ConfigParser()
    # if not config.read([args.tool_config, args.keys_config]):
    #     print("ERROR: Could not read configuration files.")
    #     sys.exit(1)

    # # 3. Push the keys into the OS memory
    # for section in config.sections():
    #     for key, value in config.items(section):
    #         os.environ[key.upper()] = value

    # 4. Start the interactive loop
    try:
        # Catch the third variable (intent_list) here!
        result, final_history, intent_list = interactive_validation_loop()
        
        if result:
            decision = result.get('response')
            confidence = result.get('confidence')

            print(f"Final Decision : {decision}")
            print(f"Confidence     : {confidence}%\n")
            
            if decision == "Yes":
                print(intent_list)
                
            elif decision == "No":
                print("The user's request violates the agent's scope.")
            
    except Exception:
        logger.exception('Unexpected error while running validation loop')
