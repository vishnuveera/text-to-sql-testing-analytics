# this file will have code or will connect to tool to generate DB query.
# we assumed that tha table name contains the testing type for api,pdf and package
import os
import re
import logging
import argparse
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

# Make sure this matches your actual import path
from llm_initialzation import create_llm, create_embeddings, call_llm_string_response
from utils import setup_logger, load_configurations
from database import retrival_schema_docs,llm_schema_docs,schema_relationships,sample_query_docs
import global_vars


logger = setup_logger("datbaseQueryGenerator","query_generator.logs")

MASTER_PROMPT = """ You are an expert SQL Database Architect.

CRITICAL INSTRUCTIONS & GUARDRAILS:

=== 0. INTELLIGENT DOMAIN ROUTING (CONTEXT INFERENCE) ===
- DOMAIN VOCABULARY MAP: You must infer which domains to query based on the specific vocabulary used in the user's intent. 
  * Trigger WEB: If the intent mentions "screen", "page", "UI", "browser", "flow", or specific UI elements (e.g., "login", "dashboard", "checkout").
  * Trigger API: If the intent mentions "endpoint", "payload", "response", "request", "JSON", "HTTP", or "status code".
  * Trigger PDF: If the intent mentions "document", "template", "visual baseline", or "text extraction".
  * Trigger PACKAGE: If the intent mentions "bundle", "suite", or "package". (Note: Packages can contain Web/API/PDF tests, so if WEB is triggered, you must also include the PACKAGE domain to find screens tested within packages).
- EXCLUSION MANDATE: You MUST exclude domains that are irrelevant to the user's context. 

=== 1. STRICT DOMAIN ISOLATION & TABLE NAMING ===
- NO CROSS-DOMAIN JOINS: You must never create SQL JOINs between different testing domains. WEB joins with WEB, API with API, etc.
- STRICT SINGLE-DOMAIN SCOPE: You will only generate a query for ONE testing domain at a time. NEVER use UNION ALL to combine WEB, API, PDF, or PACKAGE domains together. 
  * EXCEPTION: Within the PACKAGE domain ONLY, you are allowed to use UNION ALL to combine scenario step data (packagescenariorundata) and API step data (packageapirundata) into a unified package report.
- EXACT COLUMN NAMES: You MUST use the exact column names precisely as they are listed in the schema columns list. DO NOT guess, abbreviate, or hallucinate logical column names.
- NO DOMAIN COLUMN HALLUCINATION: The tables inherently represent their domains (e.g., the 'run' table is exclusively for WEB, 'apirun' is exclusively for API). DO NOT attempt to filter by a nonexistent 'domain' column in your WHERE clauses (e.g., DO NOT write "WHERE domain = 'WEB'").

DIRECT ID FILTERING: You are provided with a "Target AppID" right before the User Intent. You MUST use this exact ID to filter your queries directly on the primary execution tables (e.g., `WHERE appid = 42`). Do not join any workspace or application mapping tables.

=== 2. JOIN LOGIC & RELATIONAL ACCURACY ===
- PRIMARY/FOREIGN KEYS ONLY: You MUST join tables using their explicit Primary Keys and Foreign Keys (e.g., run.runid = rundetail.runid). 
- NO ATTRIBUTE JOINS: DO NOT join on attribute columns like 'baseline' or 'result', which may be NULL in child tables.
- MINIMUM TABLES: Identify and use ONLY the minimum required tables to answer the intent. Avoid unnecessary joins and unused columns.
- STRICT ALIAS MATCHING: Every single column prefix in the SELECT clause (e.g., 'r.runid') MUST have a corresponding table alias explicitly defined in your FROM or JOIN clauses. If you optimize by removing the parent 'run r' table, you CANNOT select 'r.runid'. You MUST use the child's ID instead (e.g., 'rd.runid').

=== 3. CTE SYNTAX & TIME-BASED FILTERING ===
- NO LITERAL TIME WORDS: NEVER use words like 'latest', 'last', or 'recent' as literal string values in a WHERE clause (e.g., DO NOT write 'WHERE baseline = 'latest'').
- SCALAR CTEs FOR TIME: If the intent involves a single version, use a simple CTE to return JUST the single scalar value (e.g., 'SELECT baseline FROM run ORDER BY rundate DESC LIMIT 1'). Then, apply that scalar value in the main query's WHERE clause (e.g., 'WHERE r.baseline = (SELECT baseline FROM LatestWebCTE)').
- LIST CTE FILTERING: If a CTE returns a list of IDs (e.g., finding the run IDs for the "last 10 runs"), you MUST apply it using an 'IN' clause in the main query's WHERE statement (e.g., 'WHERE rd.runid IN (SELECT runid FROM Last10WebRunsCTE)'). DO NOT use a LEFT JOIN to filter a CTE list, as it will break the filter.
- EXPLICIT BASELINES ONLY: The 'baseline' column is used for versioning. ONLY filter by 'baseline' if the user explicitly asks for the "latest baseline", "current baseline", or a specific version. If the user asks for historical counts (e.g., "last 10 runs", "all failed runs"), DO NOT apply a baseline filter. Just order by the run date and apply the LIMIT.
- TOP-LEVEL CTEs ONLY: If you use CTEs (WITH clauses) alongside a UNION ALL, you MUST define ALL CTEs at the very top of the query, separated by commas. NEVER place a "WITH" keyword inside or after a UNION ALL block.

=== 4. HUMAN READABILITY & UNIFIED REPORTING ===
- RESOLVE IDs TO NAMES (IRONCLAD MAPPING): NEVER return raw IDs for a report. You MUST join to the master definition tables and use these EXACT columns for the 'Test_Case_Name':
  * For WEB (join 'dataset'): use 'datasetname'. DO NOT use 'scenarioname'.
  * For API (join 'api_details'): use 'api_name'
  * For PDF (join 'pdftemplatedetails'): use 'pdftemplatename'
  * For PACKAGE (join 'packagedata'): The packagerundetail table is polymorphic. You MUST use a CASE statement based on the 'type' column to select the name (e.g., `CASE WHEN prd.type='api' THEN pd.api_name ELSE pd.scenario_name END AS Test_Case_Name`). You must also join packagedata handling both conditions: `ON ((prd.type='api' AND prd.apiid=pd.apiid) OR (prd.type='scenario' AND prd.scenarioid=pd.scenarioid))`.
- DOMAIN LABELING & NULL PADDING: Inject the domain name as a hardcoded string in the first column (e.g., 'WEB' AS Execution_Domain). If a metric (like starttime) does not exist in a domain, use 'NULL AS Start_Time'.
- SCENARIO-LEVEL TIMESTAMPS (IRONCLAD MAPPING): To report the execution time of the specific test case (not the entire batch), you MUST pull the timestamps from the child/detail execution tables. DO NOT guess the column names; use these EXACT mappings:
  * For WEB: use 'starttime' and 'endtime' from the 'rundetail' table. 
  * For API: use 'executionstarttime' and 'executionendtime' from the 'apirundetail' table. 
  * For PDF: use 'NULL AS Start_Time' and 'NULL AS End_Time'.
  * For PACKAGE: use 'executionstarttime' and 'executionendtime' from the 'packagerundetail' table.
- PREVENT DATA LOSS (LEFT JOINS): When joining execution tables to master definition tables to get human-readable names, use a LEFT JOIN to ensure deleted or orphaned records do not silently disappear from the report.
- SELECT ALL COLUMNS (FULL DATA EXTRACTION): Because the resulting data will be processed downstream by an AI critic, you MUST return EVERY column from the core execution and detail tables. You must achieve this by using table wildcards in your SELECT statement (e.g., `SELECT 'WEB' AS Execution_Domain, d.datasetname AS Test_Case_Name, r.*, rd.*`). Do NOT manually list just a few summary columns. Extract everything.

=== 5. ENUMS & CASE SENSITIVITY ===
- EXACT CASING: SQL string matching is case-sensitive. When filtering by result/status, you MUST use the exact casing specified in the schema Enums: 'pass', 'Terminated', 'Fail', 'NEW'. DO NOT default to standard title casing if the schema dictates otherwise.

=== 6. ADVANCED ANALYTIC STRATEGIES ===
- CONSISTENT/FREQUENT FAILURES: If the user asks to find test cases that "consistently fail", "fail the most", or are "unstable/flaky" over a timeframe, you MUST aggregate the data. Group by the master test case name (e.g., datasetname or api_name), count the failure IDs (e.g., COUNT(rundetailid)), and use a HAVING COUNT(...) > 1 clause to identify repeated offenders.
- SCREEN & FEATURE FAILURES (WEB): If the user asks which "screens", "features", "pages", or "UI elements" have the highest failures, DO NOT stop at the rundetail table. You MUST join down to the rundata table and the pageflow table. Group your counts by pageflow.pagename to pinpoint the exact UI screen causing the failure.
- DOWNSTREAM BLOCKERS & DEPENDENCIES: If the user asks for failures that "block downstream testing", "impact other tests", or "act as dependencies", you must use the specific structural dependency columns available for that domain. DO NOT hallucinate columns across domains.
  * For API: Use `WHERE ard.hasparent = true` or `ard.parentrundetailid IS NOT NULL`.
  * For PACKAGE: Use the caller column: `WHERE prd.Called_by IS NOT NULL`.
  * For PDF: Use the API web DTO link: `WHERE prd.dependent_api_webdto IS NOT NULL`.
  * For WEB: You must use `WHERE rd.is_dependent = true` (as this is the only dependency flag available in the rundetail schema).
- TIME & RUN THRESHOLDS: If a user asks for trends over the "last X runs" (e.g., last 10 runs), ALWAYS isolate those Run IDs first using a CTE with an ORDER BY [date_column] DESC LIMIT X. Then, apply that CTE to your main query to ensure you are only analyzing the specific historical window requested.

OUTPUT FORMAT:
Return ONLY the raw, executable SQL query. Do not wrap the output in markdown blocks (e.g., do not use ```sql). Do not provide any conversational text, prefixes, or explanations."""

# ==========================================
# 2. STATE & LAZY LOADING
# ==========================================

llm = None
embeddings = None

def build_and_search_dynamic_dbs(domain: str, query: str) -> tuple[str, str]:
    global llm, embeddings
    if llm is None or embeddings is None:
        llm = create_llm(custom_logger=logger)
        embeddings = create_embeddings(custom_logger=logger)

    global_vars.is_web_selected = (domain == "web")
    global_vars.is_api_selected = (domain == "api")
    global_vars.is_pdf_selected = (domain == "pdf")
    global_vars.is_package_selected = (domain == "package")
    
    target_domains = set()
    if global_vars.is_web_selected: target_domains.add("web")
    if global_vars.is_api_selected: target_domains.add("api")
    if global_vars.is_pdf_selected: target_domains.add("pdf")
    if global_vars.is_package_selected: target_domains.add("package")
    
    if any([global_vars.is_web_selected, global_vars.is_api_selected, global_vars.is_pdf_selected]):
        target_domains.add("package")

    active_table_names = set() 
    domains_mapping = {d: {"texts": [], "ids": []} for d in target_domains}

    for index, doc in enumerate(retrival_schema_docs, start=1):
        content = doc.page_content
        match = re.search(r"Table:\s*([a-zA-Z0-9_]+)\.", content)
        table_name = match.group(1).lower() if match else "unknown_table"

        if table_name.startswith("api") or "_api_" in table_name: doc_domain = "api"
        elif table_name.startswith("pdf"): doc_domain = "pdf"
        elif table_name.startswith("package") or "temppackage" in table_name: doc_domain = "package"
        else: doc_domain = "web"

        if doc_domain in target_domains:
            domains_mapping[doc_domain]["texts"].append(content)
            domains_mapping[doc_domain]["ids"].append(str(index))

    query_vector = embeddings.embed_query(query)
    for d, data in domains_mapping.items():
        if data["texts"]: 
            db = Chroma(collection_name=f"schema_map_{d}", embedding_function=embeddings)
            db.add_texts(texts=data["texts"], ids=data["ids"])
            
            results = db._collection.query(query_embeddings=[query_vector], n_results=10)
            
            for chunk in results["documents"][0]:
                match = re.search(r"Table:\s*([a-zA-Z0-9_]+)\.", chunk)
                if match: 
                    active_table_names.add(match.group(1).lower())

    active_schemas_context = ""
    
    for table in active_table_names:
        detailed_schema = f"Table: {table}. Details unavailable."
        
        for doc in llm_schema_docs:
            if f"Table: {table}." in doc.page_content:
                detailed_schema = doc.page_content
                break
        
        active_schemas_context += f"{detailed_schema}\n"

    filtered_relationships = [
        f"- {condition}" for t1, t2, condition in schema_relationships 
        if t1.lower() in active_table_names and t2.lower() in active_table_names
    ]
    relationships_context = "\n".join(filtered_relationships) or "- No explicit joins available for retrieved tables."

    return active_schemas_context, relationships_context

def get_initial_sql_messages(domain: str, refined_intent: str, appid: str) -> list:
    """Builds the vector context and creates the initial prompt array."""
    logger.info(f"[{domain.upper()}] Building Vector Context...")
    
    # We still search the vector DB using the intent text to get the execution tables
    active_schemas, active_relations = build_and_search_dynamic_dbs(domain, refined_intent)
    
    final_schema_context = "--- DOMAIN TABLES ---\n" + active_schemas
    
    prompt_template = PromptTemplate(
        input_variables=["intent", "schemas", "relationships", "appid"], 
        template=MASTER_PROMPT + "\n\n=== SCHEMAS ===\n{schemas}\n\n=== RELATIONSHIPS ===\n{relationships}\n\nTarget AppID: {appid}\nUser Intent: {intent}\nSQL Query:"
    )
    
    # Explicitly pass the appid into the LLM prompt!
    initial_prompt = prompt_template.format(
        intent=refined_intent, 
        schemas=final_schema_context, 
        relationships=active_relations,
        appid=appid
    )
    
    return [{"role": "user", "content": initial_prompt}]

def generate_sql_from_messages(domain: str, messages: list) -> str:
    """Takes the message history, calls the LLM, and returns clean SQL."""
    global llm
    if llm is None:
        llm = create_llm(custom_logger=logger)
        
    logger.info(f"[{domain.upper()}] Calling LLM to generate SQL...")
    raw_response = call_llm_string_response(messages, llm, custom_logger=logger)
    clean_sql = re.sub(r'\[?(WEB|API|PDF|PACKAGE)\]?\.', '', raw_response.replace("```sql", "").replace("```postgresql", "").replace("```", "").strip(), flags=re.IGNORECASE)
    
    return clean_sql

def get_one_shot_example(domain: str, intent: str) -> str:
    """Searches the sample documents for a similar intent and returns the SQL."""
    global embeddings
    if embeddings is None:
        embeddings = create_embeddings(custom_logger=logger)
        
    # Filter the docs down to just the current domain
    domain_docs = [doc for doc in sample_query_docs if doc.metadata.get("domain") == domain.lower()]
    
    if not domain_docs:
        return ""
        
    # Create a temporary mini-database just for these samples
    sample_db = Chroma.from_documents(documents=domain_docs, embedding=embeddings)
    
    # Search for the most relevant sample
    results = sample_db.similarity_search(query=intent, k=1)
    
    if results:
        best_match = results[0]
        example_sql = best_match.metadata.get("sql", "")
        example_intent = best_match.page_content
        
        return f"Example Goal: {example_intent}\nExample SQL:\n{example_sql}"
    
    return ""

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
    print("TESTING SQL GENERATOR (DICTIONARY PAYLOAD)")
    print("="*50)

    test_payload = {
        'web': 'Retrieve a report of failed test cases for the latest baseline in the Mounikalocal workspace for WEB testing.', 
        'api': 'Retrieve a report of failed test cases in the latest baseline for the Mounikalocal workspace with API testing.', 
        'pdf': 'Retrieve a report of failed test cases in the latest baseline for the "Mounikalocal" workspace under PDF testing.', 
        'package': 'Retrieve a report of failed test cases in the latest baseline for the "Mounikalocal" workspace and "PACKAGE" testing type.'
    }
    
    try:
        # Loop through the dictionary just like the orchestrator will
        for domain, intent in test_payload.items():
            print(f"\n--- TESTING DOMAIN: {domain.upper()} ---")
            print(f"USER INTENT: {intent}")
            
            print("1. Building Context and Prompts...")
            messages = get_initial_sql_messages(domain, intent, "43920720")
            
            print("2. Calling LLM to generate SQL...")
            generated_sql = generate_sql_from_messages(domain, messages)
            
            print("=== GENERATED SQL ===")
            print(generated_sql)
            print("=====================")
        
        print("\n Full Dictionary Test Complete!")
        
    except Exception as e:
        print(f"\n Generator test failed: {e}")
        logger.exception("Unit test failed")