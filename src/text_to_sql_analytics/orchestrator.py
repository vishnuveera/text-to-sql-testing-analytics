import os
import json
import sys
import argparse
import concurrent.futures
from typing import TypedDict, List, Dict, Any

from utils import setup_logger, load_configurations
logger = setup_logger("mainpipeline","orchestrator.logs")

from intentClassifcationAndFilter import validate_user_intent, get_menu_selection, filter_testing_types, set_testing_type_globals
from intentRefinement import intent_refinement
import global_vars
from llm_initialzation import create_llm
from databaseQueryGenerator import generate_sql_from_messages, get_initial_sql_messages
from databaseQueryExecutor import execute_and_heal, fetch_user_workspaces, fetch_appids_for_workspaces
from processUserQuery import process_all_domains

def phase_1_worker(domain: str, intent: str, appid: str):
    """Uses your existing functions to get context and generate the first SQL draft."""
    
    #  Pass the appid down into get_initial_sql_messages
    messages = get_initial_sql_messages(domain, intent, appid) 
    
    sql = generate_sql_from_messages(domain, messages)
    # Save the LLM's response to history
    messages.append({"role": "assistant", "content": sql})
    return sql, messages

def run_pipeline():
    print("DYNAMIC SQL GENERATION PIPELINE")

    # STEP 1: GATHER INITIAL INPUTS
    current_userid = input("Please enter your User ID (e.g., 43920821): ").strip()
    user_query = input("Enter your testing analytics query: ").strip()
    
    if not current_userid or not user_query:
        print("Error: User ID and Query are required. Exiting.")
        sys.exit(1)

    # STEP 2: DYNAMIC MENUS
    user_workspaces = fetch_user_workspaces(current_userid)
    if not user_workspaces:
        print(f"Error: No workspaces found in database for User ID {current_userid}.")
        sys.exit(1)
        
    selected_workspaces = get_menu_selection("SELECT WORKSPACE(S)", user_workspaces)
    if 'exit' in selected_workspaces: sys.exit(0)

    # 💡 THIS IS WHERE YOU USE IT!
    # The moment the user selects "Mounikalocal", we fetch the AppID.
    resolved_appids = fetch_appids_for_workspaces(selected_workspaces)
    
    if not resolved_appids:
        print("Error: Could not resolve AppIDs for the selected workspaces. Exiting.")
        sys.exit(1)
        
    # Convert the list of IDs (e.g., ['42']) into a clean string (e.g., "42")
    appid_str = ", ".join(resolved_appids) 
    workspace_str = ", ".join(selected_workspaces) # Keep this just for the menus/logging

    filtered_types = filter_testing_types(user_query)
    if global_vars.REQUIRE_DOMAIN_MENU:
        selected_testing_types = get_menu_selection("SELECT TESTING TYPE(S)", filtered_types)
        if 'exit' in selected_testing_types: sys.exit(0)
    else:
        # Silently adopt whatever the filter returned
        selected_testing_types = filtered_types

    # STEP 3: INTENT VALIDATION LOOP
    print(" INITIATING AI PIPELINE...")

    
    workspace_str = ", ".join(selected_workspaces)
    testing_str = ", ".join(selected_testing_types)
    history = []
    
    while True:
        enriched_query = (
            f"User Query: {user_query}\n\n"
            f"[CRITICAL SYSTEM NOTE: The user has already explicitly selected "
            f"Workspace(s): '{workspace_str}' and Testing Type(s): '{testing_str}' "
            f"through the UI menus. You MUST consider these two data parameters "
            f"FULLY SATISFIED. DO NOT ask the user to provide them again.]"
        )
        
        logger.info("Validating intent...")
        validation_state = validate_user_intent(enriched_query, selected_workspaces, history)
        decision = validation_state.get('response')
        history = validation_state.get('history', [])
        
        if decision == "Yes":
            break 
        elif decision == "No":
            print("\nRequest rejected by Validator: Out of scope.")
            sys.exit(0)
        else:
            user_reply = input(f"\nAgent asks: {decision}\nYour reply (or 'exit'): ").strip()
            if user_reply.lower() == 'exit': sys.exit(0)
            user_query = f"{user_query}. {user_reply}"

    # ==========================================
    # STEP 4: INTENT REFINEMENT (The Router)
    # ==========================================
    clean_list = [
        f"Target AppID(s): {appid_str}", 
        f"Testing Types: {testing_str}", 
        f"User Query: {user_query}"
    ]
    
    logger.info("Refining intent into domain dictionary...")
    # This now returns your dictionary: {'web': 'intent...', 'api': 'intent...'}
    refined_intents_dict = intent_refinement(clean_list)
    
    if not refined_intents_dict or not isinstance(refined_intents_dict, dict):
        print("Error: Refinement failed to output a valid domain dictionary.")
        sys.exit(1)

    # ==========================================
    # STEP 5: PHASE 1 - CONCURRENT SQL GENERATION
    # ==========================================
    print("\n" + "="*60)
    print("PHASE 1: GENERATING INITIAL SQL QUERIES...")
    print("="*60)
    
    generated_payloads = {}
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_domain = {
            #  Pass the appid_str as the 3rd argument here!
            executor.submit(phase_1_worker, domain, intent, appid_str): domain 
            for domain, intent in refined_intents_dict.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                # Returns the SQL and the message history for that domain
                sql, messages = future.result()
                generated_payloads[domain] = {"sql": sql, "messages": messages}
                print(f" Generated SQL for {domain.upper()}")
            except Exception as exc:
                print(f" Generation crashed for {domain.upper()}: {exc}")

    # ==========================================
    # STEP 6: PHASE 2 - EXECUTION & SELF-HEALING
    # ==========================================
    print("\n" + "="*60)
    print("PHASE 2: EXECUTING & HEALING AGAINST DATABASE...")
    print("="*60)

    if not generated_payloads:
        print("No valid SQL was generated. Exiting.")
        sys.exit(1)

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_domain = {
            # Pass refined_intents_dict[domain] as the 4th argument!
            executor.submit(execute_and_heal, domain, payload["sql"], payload["messages"], refined_intents_dict[domain]): domain 
            for domain, payload in generated_payloads.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                result = future.result() 
                print(f"\n --- STREAMED UPDATE: {domain.upper()} FINISHED ---")
                
                if result["status"] == "success":
                    print(f"Attempts Needed : {result['attempts']}/3")
                    print(f"Final SQL       :\n{result['sql']}\n")
                    
                    data = result.get('data', [])
                    print(f"Data Retrieved  : {len(data)} rows.")
                    
                    generated_payloads[domain]["data"] = data
                    
                    # if data:
                    #     print("\n--- DATABASE RESULTS ---")
                    #     print(json.dumps(data, indent=2, default=str))
                    #     print("------------------------\n")
                else:
                    print(f"FAILED after {result['attempts']} attempts.")
                    print(f"Last Attempted SQL:\n{result['sql']}")
                    print(f"Database Error:\n{result['error']}")
                    # Save empty list so Phase 3 doesn't crash
                    generated_payloads[domain]["data"] = []
                    
            except Exception as exc:
                print(f"Execution crashed for {domain.upper()}: {exc}")
                generated_payloads[domain] = {"data": []}

    print("\n" + "="*60)
    print(" ALL DOMAINS PROCESSED SUCCESSFULLY")
    print("="*60 + "\n")


    # ==========================================
    # STEP 7: SAVE DEBUG JSONS & UPDATE GLOBALS
    # ==========================================
    print("\n" + "="*60)
    print("PHASE 3: SAVING INTERMEDIATE JSONS & RUNNING CRITIC NODE...")
    print("="*60)

    # Create a folder for the debug JSONs if it doesn't exist
    os.makedirs("Debug_Output", exist_ok=True)

    # 1. Loop through the successful payloads and write them to disk
    for domain, payload in generated_payloads.items():
        if "data" in payload and payload["data"]:
            file_path = f"Debug_Output/{domain}_db_results.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({"data": payload["data"]}, f, indent=4, default=str)
                
            print(f"Saved {domain.upper()} intermediate data to: {file_path}")

            # 2. Dynamically update global_vars with the file paths and the exact LLM intent
            domain_intent = refined_intents_dict.get(domain, user_query)
                
            if domain == 'web':
                global_vars.web_json = file_path
                global_vars.web_user_intent = domain_intent
            elif domain == 'api':
                global_vars.api_json = file_path
                global_vars.api_user_intent = domain_intent
            elif domain == 'pdf':
                global_vars.pdf_json = file_path
                global_vars.pdf_user_intent = domain_intent
            elif domain == 'package':
                global_vars.package_json = file_path
                global_vars.package_user_intent = domain_intent

    # ==========================================
    # STEP 8: RUN THE CRITIC NODE
    # ==========================================
    print("\nRunning AI Data Validator...")
        
    # Initialize the LLM specifically for the validation phase
    validator_llm = create_llm(custom_logger=logger)

    try:
        final_results = process_all_domains(validator_llm)
            
        for result in final_results:
            print(f"\n--- FINAL ANSWER: {result['domain'].upper()} ---")
            print(json.dumps(result["final_answer"], indent=2, default=str))
                
    except Exception as e:
        print(f"\nCritical Error in Validation Phase: {e}")

    print("\n" + "="*60)
    print(" PIPELINE COMPLETE")
    print("="*60 + "\n")

# This remains completely un-indented at the bottom of the file
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Full Analytics Pipeline")
    parser.add_argument('--tool-config', required=True, help="Path to tool configurations")
    parser.add_argument('--keys-config', required=True, help="Path to keys configurations")
    args = parser.parse_args()
    
    try:
        load_configurations(args.tool_config, args.keys_config)
    except Exception as e:
        logger.error(f"Failed to load configurations: {e}")
        raise
        
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print("\nPipeline terminated by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception("Fatal error in main pipeline")