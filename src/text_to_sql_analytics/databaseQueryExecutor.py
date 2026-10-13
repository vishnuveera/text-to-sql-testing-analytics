#this file will have code for execution of Query in DB

import os
import re
import logging
import psycopg2
import psycopg2.extras
import argparse
from azure.identity import ManagedIdentityCredential
from utils import setup_logger, load_configurations
from databaseQueryGenerator import get_initial_sql_messages, generate_sql_from_messages, get_one_shot_example

logger = setup_logger("datbaseQueryExecutor","query_executor.logs")

def get_db_connection():
    """Smart connection router relying entirely on environment variables from .cfg files."""
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('POSTGRES_PORT', '5432')
    db_name = os.getenv('POSTGRES_DBNAME')
    db_user = os.getenv('POSTGRES_USERNAME')
    
    if os.getenv('DEPLOYMENT_ENV') != 'local':
        logger.info("Connecting to Database via Azure Managed Identity (Production Mode)")
        try:
            credential = ManagedIdentityCredential(client_id=os.getenv('UAMI_CLIENT_ID'))
            token = credential.get_token(os.getenv('AZURE_POSTGRESQL_SCOPE')).token
            
            return psycopg2.connect(
                dbname=db_name, 
                user=db_user, 
                password=token,
                host=db_host,
                port=db_port,
                sslmode="require"
            )
        except Exception as e:
            logger.error(f"Azure Managed Identity connection failed: {str(e)}")
            raise
    else:
        logger.info("Connecting to Database via Local Credentials (Demo Mode)")
        try:
            db_password = os.getenv('POSTGRES_PASSWORD', '')
            return psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
        except Exception as e:
            logger.error(f"Local database connection failed: {str(e)}")
            raise

def fetch_user_workspaces(userid: str) -> list:
    """Fetches the available workspaces (apps) for the current user."""
    query = f"""
        SELECT a.appname 
        FROM userconfigration uc 
        JOIN applications a ON uc.appid = a.appid 
        WHERE uc.userid = '{userid}';
    """
    try:
        # execute_query now just returns the rows directly!
        rows = execute_query(query)
        workspaces = [row['appname'] for row in rows]
        return workspaces
        
    except Exception as e:
        # If the database throws an error, we catch it here and return an empty list
        logger.error(f"Failed to fetch workspaces for user {userid}: {e}")
        return []

def fetch_appids_for_workspaces(workspace_names: list) -> list:
    """Takes a list of workspace names and returns a list of their corresponding appids."""
    appids = []
    
    # Format the names for a SQL IN clause (e.g., 'Mounikalocal', 'MLocal')
    formatted_names = ", ".join([f"'{name}'" for name in workspace_names])
    query = f"SELECT appid FROM applications WHERE appname IN ({formatted_names})"
    
    try:
        # Use your existing, updated execute_query function!
        rows = execute_query(query)
        for row in rows:
            appids.append(str(row['appid']))
            
    except Exception as e:
        logger.error(f"Failed to fetch AppIDs for workspaces {workspace_names}: {e}")
        
    return appids

def execute_query(query: str):
    """Executes the generated SQL query against the database and returns JSON-friendly dicts."""
    if not re.match(r"^\s*(SELECT|WITH)\b", query, flags=re.IGNORECASE):
        raise Exception("SECURITY BLOCK: Only SELECT queries are permitted.")
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        logger.info("Executing generated SQL query...")
        cur.execute(query)
        
        # Note: If your AI ever generates an INSERT/UPDATE, fetchall() will throw an error. 
        extracted_rows_list = cur.fetchall()
        cur.close()
        
        logger.info(f"Query executed successfully. Retrieved {len(extracted_rows_list)} rows.")
        clean_rows = [dict(row) for row in extracted_rows_list]
        
        # RETURN 1: On success, just return the raw data array!
        return clean_rows
    
    except psycopg2.errors.UndefinedColumn as e:
        error_msg = f"Missing Column Error: {str(e).strip()}"
        logger.warning(error_msg)
        #  RETURN 2: We MUST raise this so the Executor catches it and triggers the AI!
        raise Exception(error_msg)

    except (Exception, psycopg2.DatabaseError) as error:
        error_msg = f"Database Error: {str(error).strip()}"
        logger.exception("Exception occurred during database execution")
        # RETURN 3: We MUST raise this too!
        raise Exception(error_msg)
    
    finally:
        if conn is not None:
            conn.close()

# def execute_and_heal(domain: str, current_sql: str, messages: list) -> dict:
#     """
#     Takes pre-generated SQL. Tries to run it. 
#     If it fails, it uses your existing 'generate_sql_from_messages' to heal it.
#     """
#     max_attempts = 3
    
#     for attempt in range(1, max_attempts + 1):
#         try:
#             logger.info(f"[{domain.upper()}] Executing DB Query (Attempt {attempt}/{max_attempts})...")
            
#             # 1. TRY TO RUN THE SQL USING YOUR EXISTING FUNCTION
#             db_results = execute_query(current_sql) 
            
#             # SUCCESS!
#             logger.info(f"[{domain.upper()}] Query Execution Successful!")
#             return {
#                 "domain": domain,
#                 "status": "success",
#                 "sql": current_sql,
#                 "data": db_results,
#                 "attempts": attempt
#             }
            
#         except Exception as e:
#             error_msg = str(e)
#             logger.warning(f"[{domain.upper()}] SQL Execution Failed: {error_msg}")
            
#             # 2. IF IT FAILS, HEAL IT USING YOUR EXISTING FUNCTION
#             if attempt < max_attempts:
#                 logger.info(f"[{domain.upper()}] Calling LLM to heal SQL...")
                
#                 # Append the bad SQL and the error to the message history
#                 messages.append({"role": "assistant", "content": current_sql})
#                 messages.append({
#                     "role": "user", 
#                     "content": f"The query failed with the following database error:\n{error_msg}\n\nPlease fix the query and return ONLY the corrected, executable SQL."
#                 })
                
#                 # 💡 Generate the new SQL using the function you already have!
#                 current_sql = generate_sql_from_messages(domain, messages)
                
#             else:
#                 logger.error(f"[{domain.upper()}] Max attempts reached. Failed to execute.")
#                 return {
#                     "domain": domain,
#                     "status": "failed",
#                     "sql": current_sql,
#                     "error": error_msg,
#                     "attempts": attempt
#                 }

def execute_and_heal(domain: str, current_sql: str, messages: list, original_intent: str) -> dict: 
    """Takes pre-generated SQL. Tries to run it. If it fails, uses one-shot RAG to heal it."""
    max_attempts = 3
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"[{domain.upper()}] Executing DB Query (Attempt {attempt}/{max_attempts})...")
            db_results = execute_query(current_sql) 
            
            logger.info(f"[{domain.upper()}] Query Execution Successful!")
            return {
                "domain": domain, "status": "success", "sql": current_sql,
                "data": db_results, "attempts": attempt
            }
            
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[{domain.upper()}] SQL Execution Failed: {error_msg}")
            
            if attempt < max_attempts:
                logger.info(f"[{domain.upper()}] Calling LLM to heal SQL...")
                
                one_shot_context = get_one_shot_example(domain, original_intent)
                
                healing_prompt = f"The query failed with the following database error:\n{error_msg}\n\n"
                
                if one_shot_context:
                    healing_prompt += f"To help you fix this, here is a verified working example for a similar goal in the {domain.upper()} domain:\n{one_shot_context}\n\n"
                    
                healing_prompt += "Please fix the query and return ONLY the corrected, executable SQL."
                
                messages.append({"role": "assistant", "content": current_sql})
                messages.append({"role": "user", "content": healing_prompt})
                
                current_sql = generate_sql_from_messages(domain, messages)
                
            else:
                logger.error(f"[{domain.upper()}] Max attempts reached. Failed to execute.")
                return {"domain": domain, "status": "failed", "sql": current_sql, "error": error_msg, "attempts": attempt}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run SQL Generator Unit Test")
    parser.add_argument('--tool-config', required=True, help="Path to tool configurations")
    parser.add_argument('--keys-config', required=True, help="Path to keys configurations")
    args = parser.parse_args()
    try:
        load_configurations(args.tool_config, args.keys_config)
    except Exception as e:
        logger.error(f"Failed to load configurations: {e}")
        raise

    print("\n" + "="*50)
    print(" TESTING DATABASE EXECUTOR (PHASE 2 ONLY)")
    print("="*50)

    test_domain = "web"
    
    #  MOCKING PHASE 1: We pretend the LLM already generated this.
    # To test the self-healing, intentionally make a syntax error here 
    # (e.g., change 'r.result' to a fake column like 'r.fake_column')
    mock_sql = "WITH LatestBaselineCTE AS ( SELECT baseline FROM run WHERE appid = (SELECT appid FROM applications WHERE appname = 'Mounikalocal') ORDER BY rundate DESC LIMIT 1)SELECT 'WEB' AS Execution_Domain,ds.datasetname AS Test_Case_Name,r.result AS Overall_Result,r.starttime AS Start_Time,r.endtime AS End_Time,rd.result AS Scenario_Result,rd.starttime AS Scenario_Start_Time,rd.endtime AS Scenario_End_Time FROM run r LEFT JOIN rundetail rd ON r.runid = rd.runid LEFT JOIN dataset ds ON rd.scenarioid = ds.datasetid WHERE  r.baseline = (SELECT baseline FROM LatestBaselineCTE) AND r.result = 'Fail' AND rd.result = 'Fail';"
    # We also have to mock the history so the LLM has context if it needs to heal
    mock_messages = [
        {"role": "user", "content": "Generate SQL for failed web runs."},
        {"role": "assistant", "content": mock_sql}
    ]
    
    print(f"TEST DOMAIN : {test_domain.upper()}")
    print(f"TEST SQL    :\n{mock_sql}\n")
    
    try:
        print("Starting Execution and Healing Loop...\n")
        
        # Pass the pre-generated SQL and history to the Executor
        result_payload = execute_and_heal(test_domain, mock_sql, mock_messages)
        
        print("\n=== FINAL RESULT PAYLOAD ===")
        print(f"Status  : {result_payload.get('status').upper()}")
        print(f"Attempts: {result_payload.get('attempts')}/3")
        print(f"SQL     :\n{result_payload.get('sql')}\n")
        
        if result_payload.get("status") == "success":
            data = result_payload.get('data', [])
            print(f"Data    : {len(data)} rows retrieved.")
        else:
            print(f"Error   : {result_payload.get('error')}")
            
        print("============================")
        print("\n Executor Test Complete!")
        
    except Exception as e:
        print(f"\n Executor test failed catastrophically: {e}")
        logger.exception(" test failed")