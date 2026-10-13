from langchain_core.documents import Document

retrival_schema_docs = [
    Document(
    page_content="Table: run. Columns: runid(Primary Key), appid, baseurl, createdby, result, rundate, screen_shot_type, browser, endtime, starttime, runtime, kill, template_name, complete_count, fail_count, orfail_count, baseline (Used to filter versions. Find the latest by sorting 'rundate' DESC), dependentapirunid. Description: Master table for Web scenario executions recording overall run status, screen_shot_type stores for which result we are storing the screenshots for example(OFSS-OrFail, ESS-Error,WSS-All,NO)."
    ),

    Document(
    page_content="Table: rundetail. Columns: rundetailid(Primary Key), baseline, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), runid, runsequence, scenariodatsetid, scenarioid, scenariotype, batchid, is_dependent, endtime, starttime, runtime, env_name, deletedby, deleteddate, isdeleted, createdtime, script. Description: Stores Web scenario execution results, times, and screenshots for individual scenarios and TC within a bundle/scenario run."
    ),

    Document(
    page_content="Table: rundata. Columns: rundataid(Primary Key), datasetid, pageflowid, pagerunsequence, result, rundetailid, scenariodataid, endtime, starttime, runtime. Description: Captures step-by-step execution data specifically at the page or flow level during a scenario run for Web scenario executions."
    ),

    Document(
    page_content="Table: rundataasssertiondetails. Columns: run_data_assertion_detailsid(Primary Key), actualvalue, asserttype, dataset_id, elementsequence, element_type, elementlabel, end_time, expectedvalue, inputvalue, message, pageflow_id, property_id, result, rundataid, run_detail_id, start_time, runtime, dateformat, errormessage. Description: Captures exact pass/fail logic, expected versus actual values, and precise assertion outcomes during Web scenario executions."
    ),

    Document(
    page_content="Table: data. Columns: dataid(Primary Key), assertid, assertionenabled, dataset_id, expectedvalue, isdeleted, value, createdby, createddate, deletedby, deleteddate, isenabled, operator, retryattempt, dataname, datatype, dateformat. Description: Defines specific test data values, expected outcomes, database connections, and assertion logic used by datasets for Web scenario executions."
    ),

    Document(
    page_content="Table: dataset. Columns: datasetid(Primary Key), appid, baseline, createdby, createddate, datasetname(CRITICAL: Use this column when asked for the Test Case Name), isdefaultvalue, pageno, pageflowid, softdelete, deletedby, deleteddate, systemdataset, app_id, base_line, created_by, created_date, dataset_name, deleted_by, deleted_date, isdefault_value, page_no, pageflow_id, iscloned, validationflagatscan. Description: Represents a logical grouping of test data mapping to specific applications and UI page flows for Web scenario executions."
    ),

    Document(
    page_content="Table: scenariodataset. Columns: scdatasetid(Primary Key), createddate, isdeleted, scenariodatasetname, scenarioid, createdby, deletedby, deleteddate, iscloned. Description: Junction table linking test scenarios to their respective datasets for Web scenario executions."
    ),

    Document(
    page_content="Table: scenariodetails. Columns: id(Primary Key), baseline, created_by, created_date, isdeleted, pageflowid, pagesequence, scenarioid, version, deletedby, deleteddate. Description: Defines the step-by-step sequence of UI page flows or actions that make up a single test scenario for Web scenario executions."
    ),

    Document(
    page_content="Table: scenarios. Columns: scenarioid(Primary Key), appid, baseline, cloneid, createdby, createddate, isdeleted, scenarioname (This is the parent scenario wrapper. Do NOT use this for the specific Test Case Name), scenariosequence, custom, deletedby, deleteddate. Description: Master repository for individual test scenarios related to Web scenario executions."
    ),

    Document(
    page_content="Table: scenariobatch. Columns: sc_batch_id(Primary Key), appid, baseline, batchname, createddate, createdby, deletedby, deleteddate, isdeleted, batchsequence, is_scenario_execution_parallel,abort. Description: Defines bundles (batches) of scenarios, allowing grouped and potentially parallel execution of tests in Web scenario executions."
    ),

    Document(
    page_content="Table: scenariobatchdata. Columns: scbatchdatid(Primary Key), createdby, createddate, deletedby, deleteddate, isdeleted, sc_batch_id, scenarioid, scenariobatchdataseq. Description: Maps which specific test scenarios are included inside a defined bundle or batch for Web scenario executions."
    ),

    Document(
    page_content="Table: scenariobatchdatasetdata. Columns: scbatchdatasetid(Primary Key), createdby, createddate, deletedby, deleteddate, isdeleted, sc_batch_id, scdatasetid, scenarioid, scbatchdatid, scenariobatchdatasetseq. Description: Specifies exactly which datasets are used for a scenario when it is executed within a specific bundle for Web scenario executions."
    ),

    Document(
        page_content="Table: aipageflow. Columns: aipageflowid(Primary Key), aipageflowreferenceid, appid, pagename, nextpagename, actionid, actionvalue, Imagename, screenshotname, screenchanges, baseline, created_by, created_date, isbaselinerequired, isdeleted, nextpageno, pageno, pending, screenshottime, version, deletedby, deleteddate, oldaipageflowid. Description: AI-augmented page flow for visual testing."
    ),

    Document(
        page_content="Table: pageflow. Columns: pageflowid(Primary Key), pageflowreferenceid, appid, pagename, nextpagename, actionid, actionvalue, recordingfilename, modelchanges, baseline, created_by, created_date, isbaselinerequired, isscenariosgenerated, isdeleted, nextpageno, pageno, recordingtime, version, isbusinessimpacted, createdby, createddate, deletedby, deleteddate, Modeid, Oldpageflowid. Description: recorded page flow steps."
    ),

    Document(
        page_content="Table: page_flow. Columns: page_flow_id(Primary Key), pageflow_reference_id, app_id, page_name, next_page_name, action_id, action_value, recording_file_name, model_changes, baseline, created_by, created_date, deleted_by, deleted_date, is_baseline_required, is_business_impacted, is_scenarios_generated, isdeleted, next_page_no, page_no, recording_time, version. Description: Modernized schema for recorded page flow steps."
    ),
    
    Document(
    page_content="Table: package_run_variables. Columns: Run_id(Primary Key), Variable_name, Rundetail_id, Var_value. Description: Stores dynamic runtime variables generated or passed during package executions."
    ),

    Document(
    page_content="Table: package_api_run_data. Columns: Packageapirundataid(Primary Key), Apirundataid, Apidatsequence, Duration, Executionendtime, Executionstarttime, Packagerundetailid, Result, Baseline. Description: Tracks high-level execution times, sequence, and final results specifically for API tests within a package."
    ),

    Document(
    page_content="Table: packageapirunvalidation. Columns: packageapirunvalidationid(Primary Key), actualvalue, apidatasetid, duration, executionendtime, executionstarttime, expectedvalue, result, packagerundetailid, Assert_type, count, packagedependentapirundetailid, assertid, dateformat, givenregex. Description: Contains detailed API validation checks, comparing expected versus actual payloads."
    ),

    Document(
    page_content="Table: packagedata. Columns: packagedata_id(Primary Key), apiid, api_name, app_id, createdby, createddate, deletedby, deleteddate, isdeleted, package_id, package_type, packagedatasequence, scenarioid, scenario_name, scenario_type, datasetappid, isactive, isunpicked, llmgenerated. Description: Defines the composition of a package, mapping the various API, Web, and PDF scenarios that belong to it. "
    ),

    Document(
    page_content="Table: packagedatasetdata. Columns: packagedatasetid(Primary Key), apidatasetid, api_dataset_name, api_id, createdby, createddate, deletedby, deleteddate, isdeleted, package_id, packagedata_id, scdatasetid, scenario_dataset_name, scenarioid, isactive, isunpicked, llmgenerated. Description: Connects specific datasets to the APIs and scenarios mapped inside a package execution."
    ),

    Document(
    page_content="Table: packagedependent_api_run_detail. Columns: packagedependentapirundetailid(Primary Key), api_alias, api_id, api_name, data_set_alias, data_set_id, data_set_name, parent_api_id, parentapi_run_id, parent_data_set_id, request, response, result. Description: Stores information of dependent API calls executed within a package."
    ),

    Document(
    page_content="Table: packagedetails. Columns: package_id(Primary Key), appid, baseline, createddate, createdby, Deletedby, deleteddate, environment_type, isdeleted, packagesequence, abort, isactive, llmgenerated. Description: Master table for package configurations, grouping Web, API, and PDF tests together into a single execution unit."
    ),

    Document(
    page_content="Table: packagereport. Columns: packageid, branch, branchcovered, branchmissed, complexity, complexitycovered, complexitymissed, instruction, instructioncovered, instructionmissed, lines, linescovered, linesmissed, methods, methodscovered, methodsmissed, Appid, baseline, classes, classescovered, classesmissed, packagename, reportname, runid. Description: Stores code coverage analytics and metrics generated after a full package run."
    ),

    Document(
    page_content="Table: packagerun. Columns: packagerunid(Primary Key), appid, browser, duration, envtype, executedby, executeddate, executionendtime, executionstarttime, result, store_value, abort, ispackageexecutionparallel, kill, executionruntime, template_name, deviceid, baseline (Used to filter versions. Find the latest by sorting 'executeddate' DESC). Description: Master record for a package execution instance tracking overall status, environment, and parallel execution flags."
    ),

    Document(
    page_content="Table: packagerundetail. Columns: packagerundetailid(Primary Key), apidatasetid, apiid, apirunsequence, baseline, duration, ismockingenabled, packageid, packagerunid, packagerunsequence, request, response, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), runsequence, scenariodatsetid, scenarioid, type, isdependentapi, executionendtime, executionstarttime, executionruntime, Deletedby, Deletedate, Isdeleted, Called_by. Description: Logs individual step-by-step executions (Web, API, PDF) within a package run, including payloads and mock settings."
    ),

    Document(
    page_content="Table: packagerunreport. Columns: packagerunreportid(Primary Key), createddate, packagerunid, report, reportstatus, runstatus. Description: Stores generated execution reports as byte arrays and their processing statuses for package runs." 
    ),

    Document(
    page_content="Table: packagescenariorundata. Columns: packagescrundataid(Primary Key), datasetid, duration, executionendtime, executionstarttime, packagerundetailid, pageflowid, pagerunsequence, result, scenariodataid, executionruntime. Description: Captures page-level execution times  data specifically for Web/PDF scenarios inside a package."
    ),

    Document(
    page_content="Table: packagesrundataassertiondetails. Columns: packagescrundataassertiondetailsid(Primary Key), actualvalue, asserttype, dataset_id, duration, elementsequence, element_type, elementlabel, executionendtime, executionstarttime, expectedvalue, inputvalue, message, packagerundetailid, packagescrundataid, pageflow_id, result, executionruntime, dateformat, errormessage. Description: Results comparing expected and actual values for Web/PDF scenarios within package executions."
    ),

    Document(
    page_content="Table: temppackagedata. Columns: packagedata_id, apiid, api_name, app_id, createdby, createddate, datasetappid, isactive, isunpicked, package_id, package_type, packagedatasequence, llmgenerated. Description: Temporary staging table used to hold configurations for APIs and scenarios while building a package."
    ),

    Document(
    page_content="Table: temppackagedataset. Columns: packagedatasetid, apidatasetid, api_dataset_name, api_id, createdby, createddate, isactive, isunpicked, package_id, packagedata_id, llmgenerated. Description: Temporary staging table used to link datasets to APIs and scenarios while a package is actively being built."
    ),

    Document(
    page_content="Table: temppackagedetails. Columns: pkgid, appid, baseline, createddate, createdby, isactive, packagename, packagesequence, llmgenerated. Description: Used as a temporary staging table for package details configuration."
    ),

    Document(
        page_content="Table: api_body. Columns: api_body_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, isdeleted, type, value, baseline, value_source. Description: Stores the raw payload, such as JSON, sent in the API request. Maps to the master API via api_id."
    ),

    Document(
        page_content="Table: api_data. Columns: api_data_id(Primary Key), api_body_id, api_data_set_id, api_id, api_parameter_id, created_by, created_date, deleted_by, deleted_date, isdeleted, value, baseline, param_source, body_source, raw_type, isjson_present, data_assist_doc_id, db_config_id, scriptnotion. Description: connects specific test data values to datasets, parameters, and API bodies. Tracks where the data is sourced from."
    ),

    Document(
        page_content="Table: api_data_set. Columns: api_data_set_id(Primary Key), api_id, app_id, assertionenabled, created_by, created_date, data_set_name, deleted_by, deleted_date, isdeleted, apitype, baseline, assertionid, expected_value, data_set_alias, api_data_set_alias, description, generate_type, bruledesc, bruleid, brdesc, brid, clonedfromid, iscloned, criteria. Description: defining a specific test case dataset, Contains expected outcomes and business rules for evaluating the API."
    ),

    Document(
        page_content="Table: api_details. Columns: api_id(Primary Key), api_name, app_id, created_by, created_date, deleted_by, deleted_date, generate_type, isdeleted, method_type, url, apitype, baseline, is_baseline_required, api_alias, is_data_set_present, apisequence, schema_type, is_cloned_api, docname, method_name, protofile, refprotofile, request_name. Description: Master repository for every API."
    ),

    Document(
        page_content="Table: api_header_details. Columns: header_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, header_name, header_value, isdeleted, baseline, header_source, db_config_id, data_assist_doc_id, headersourcetype, script_name. Description: Stores specific headers, like Authorization or Content-Type, mapped directly to an API definition."
    ),

    Document(
        page_content="Table: api_parameter. Columns: api_parameter_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, isdeleted, issensitive, parameter_label, parameter_type, baseline,  enumpresent, generatetype, parameterdatatype, required, swaggerconstraints, userconstraints, missing. Description: Defines specific URL components like query, path, and header parameters. Tracks data types, constraints, and sensitive data flags for API executions."
    ),

    Document(
        page_content="Table: api_schema. Columns: schema_id(Primary Key), input_ignore, input_schema, output_ignore, output_schema, baseline, deleted_by, deleted_date, isdeleted, api_id, created_by, created_date. Description: Stores the strict JSON structural contracts for an API to validate request and response formats independently of test data."
    ),

    Document(
        page_content="Table: api_schemas. Columns: schema_id, api_id, created_by, created_date, deleted_by, deleted_date, input_ignore, input_schema, isdeleted, output_ignore, output_schema, baseline, input_ignore_source, input_schema_source, output_ignore_source, output_schema_source, is_input_schema_file, is_output_schema_file, schemadetails, swaggerschema, swaggeroutputschema. Description: Extended schema definition table managing strict input/output structures, swagger definitions for API execution."
    ),

    Document(
        page_content="Table: apiassertion. Columns: apiassertid(Primary Key), additionaldetails, apiasserttype, operator. Description: Defines validation types, which are then referred via assertionid in datasets for APIs."
    ),

    Document(
        page_content="Table: apidefaultvalue. Columns: id, arraydatatype, value, decimalplaces, digits, lowercase, maximumvalue, maxitems, maxlength, minimumvalue, minitems, minlength, spaces, specialchars, type, uppercase, apiid. Description: Stores fallback data generation rules and constraints for payload parameters when explicit test data is not provided for API execution."
    ),

    Document(
        page_content="Table: apirequestheaders. Columns: id(Primary Key), headername, headerdisplay_value. Description: A lookup or definition table storing standard HTTP header names and their display values for UI presentation in API execution."
    ),

    Document(
        page_content="Table: apirun. Columns: apirunid(Primary Key), apirundate, apiurl, appid, createdby, result, runtype, templatename, executionendtime, executionruntime, executionstarttime, kill, baseline (Used to filter versions. Find the latest by sorting 'apirundate' DESC). The master execution record for API tests. Description: Tracks URL run targets, execution durations, and final pass/fail results."
    ),

    Document(
        page_content="Table: apirundata. Columns: apirundataid(Primary Key), apidataid, apidatsequence, apirundetailid, baseline. Description: Sequence tracker that maps specific data inputs directly to the granular API run details during execution."
    ),

    Document(
        page_content="Table: apirundetail. Columns: apirundetailid(Primary Key), apidatasetid, apiid, apirunid, apirunsequence, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), response, request, actual_value, expected_value, is_mocking_enabled, baseline, dependent_api_webdto, is_dependent_api, standard_version, env_name, executionendtime, executionruntime, executionstarttime, specified_row, resdiffernce, hasparent, parentrundetailid, parenttype, grpcrunmode. Description: log of a single API execution step. Captures traffic payloads, actual versus expected values, mocking flags, and specific error differences."
    ),

    Document(
        page_content="Table: apirunvalidation. Columns: apirunvalidationid(Primary Key), apidatasetid, result, actualvalue, expectedvalue, baseline, apirundetailid, dependent_api_run_detail_id, count, dateformat, givenregex, assertid, expectedresult, operator. Description: Logs assertion checks during an  API execution, showing why a test failed by comparing actual values to expected patterns and operators."
    ),

    Document(
        page_content="Table: apischema. Columns: schema_id, input_ignore, input_schema, output_ignore, output_schema, deleted_by, deleted_date, isdeleted, baseline. Description: Additional configuration table storing the structural JSON definitions expected for API request inputs and response outputs."
    ),

    Document(
        page_content="Table: apivalidation. Columns: apivalidationid(Primary Key), api_data_set_id, app_id, assertionid, created_by, created_date, deleted_by, deleted_date, expectedvalue, isdeleted, dbconfigid, operator, baseline, validation_source, count, dateformat, givenregex, db_driver, db_pwd, db_username, expectedresult, data_assist_doc_id, api_mapping_id. Description: Master definition for API dataset validations. Configures expected regex matches, operators, and database connections required to validate an API response."
    ),

    Document(
        page_content="Table: pdfdataset. Columns: pdfdatasetid(Primary Key), createddate, createdby, datasetname, deletedby, isdeleted, pdffiledata, pdfid, zipfilename, temppdffiledata, baseline, isbaselined, filename. Description: Master container for a specific set of PDF test data, storing actual PDF dataset files or zip archives used during test execution."
    ),

    Document(
        page_content="Table: pdfdatasetdata. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldactualdata, fieldname, isdbquery, isdeleted, pdfdatasetid, pdffilename, pdfid, pdfsectionid, sectionname, row_validation, image, imagedata, baseline, source, dbname. Description: Maps specific fields within a PDF dataset to their expected text or image data, including flags for table-row validation."
    ),

    Document(
        page_content="Table: pdfexceldatasetdata. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldactualdata, fieldname, isdbquery, isdeleted, pdfdatasetid, pdffilename, pdfid, pdfsectionid, row_validation, sectionname, x1, x2, y1, y2, baseline, source. Description: Stores expected values and box coordinates (x1, y1, x2, y2) for extracting and validating tabular or Excel-like data from PDFs."
    ),

    Document(
        page_content="Table: pdfrun. Columns: pdfrunid(Primary Key), appid, createdby, pdfrundate, result, runtype, kill, baseline (Used to filter versions. Find the latest by sorting 'pdfrundate' DESC). Description: The master record for a PDF test execution, tracking the overall environment, run dates, and final pass/fail results."
    ),

    Document(
        page_content="Table: pdfrundata. Columns: pdfrundataid(Primary Key), actualvalue, dbid, expectedvalue, fieldname, fieldresult, isdbquery, pdfname, pdfrundetailid, sectionname, pdfsectionid, pdf_run_data, expectedfetchedvalue, assertid, isimage, baseline, source, dbname. Description: execution log for PDF tests. Records the extracted actual values against expected values, database cross-checks, and field-level pass/fail results."
    ),

    Document(
        page_content="Table: pdfrundatadetail. Columns: pdfrundatadetailid(Primary Key), pdfdataid, pdfdatsequence, pdfrundetailid. Description: A sequence tracking table that records the order in which PDF data fields were processed during a test run."
    ),

    Document(
        page_content="Table: pdfrundetails. Columns: pdfrundetailid(Primary Key), appid, pdfdatasetid, pdfdatasetname, pdfid, pdfname, pdfrunid, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), pdfrunsequence, pdftemplatename, dependent_api_webdto, baseline, envname. Description: log tracking the execution of a specific PDF template within a larger run, linking the run to the specific dataset and environment."
    ),

    Document(
        page_content="Table: pdfsectiondetails. Columns: pdfsectionid(Primary Key), border, createddate, createdby, deletedby, is_dynamic_table, isdeleted, pdfid, pdfpageno, sectionname, sequence, isuserdefined, x1, x2, y1, y2, baseline. Description: Defines the zones using exact coordinates and page numbers."
    ),

    Document(
        page_content="Table: pdftemplatedetails. Columns: pdfid(Primary Key), appid, createdatetime, createdby, deletedby, gridpdftemplatedata, isdeleted, name, originalpdftemplatedata, pdftemplatename (CRITICAL: Use this column when asked for the Test Case Name. Do NOT use 'pdfname')., updatedatetime, updatedby, tempgridpdftemplatedata, temporiginalpdftemplatedata, baseline, isbaselinerequired, isupdated. Description: Master repository for base PDF templates, storing the raw document binary data to serve as a visual baseline for comparisons."
    ),
    
    Document(
        page_content="Table: pdfvalidationdetails. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldname, image, isdbquery, isdeleted, pdfid, pdfpageno, pdfsectionid, sectionname, x1, x2, y1, y2, imagedata, baseline, source, dbname. Description: The master rulebook for a PDF template. Defines bounding boxes, expected text or image values, and assertion operators for visual and data validation."
    )
]

# Fully detailed schemas formatted as LangChain Documents.
llm_schema_docs = [
    Document(
        page_content="Table: run. Columns: runid(Primary Key), appid, baseurl, createdby, result, rundate, screen_shot_type, browser, endtime, starttime, runtime, kill, template_name, complete_count, fail_count, orfail_count, baseline (Used to filter versions. Find the latest by sorting 'rundate' DESC), dependentapirunid. Description: Master table for Web scenario executions recording overall run status, screen_shot_type stores for which result we are storing the screenshots for example(OFSS-OrFail, ESS-Error,WSS-All,NO)."
    ),
    Document(
        page_content="Table: rundetail. Columns: rundetailid(Primary Key), baseline, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), runid, runsequence, scenariodatsetid, scenarioid, scenariotype, batchid, is_dependent, endtime, starttime, runtime, env_name, deletedby, deleteddate, isdeleted, createdtime, script. Description: Stores Web scenario test case execution results, times, and screenshots for individual scenarios and TC within a bundle/scenario run, here scenariotype contains custom,choose or bundle it does not contain web,api or pdf."
    ),
    Document(
        page_content="Table: rundata. Columns: rundataid(Primary Key), datasetid, pageflowid, pagerunsequence, result, rundetailid, scenariodataid, endtime, starttime, runtime. Description: Captures step-by-step execution data specifically at the page or flow level during a scenario run for Web scenario executions."
    ),
    Document(
        page_content="Table: rundataasssertiondetails. Columns: run_data_assertion_detailsid(Primary Key), actualvalue, asserttype, dataset_id, elementsequence, element_type, elementlabel, end_time, expectedvalue, inputvalue, message, pageflow_id, property_id, result, rundataid, run_detail_id, start_time, runtime, dateformat, errormessage. Description: Captures exact pass/fail logic, expected versus actual values, and precise assertion outcomes during Web scenario executions."
    ),
    Document(
        page_content="Table: data. Columns: dataid(Primary Key), assertid, assertionenabled, dataset_id, expectedvalue, isdeleted, value, createdby, createddate, deletedby, deleteddate, isenabled, operator, retryattempt, dataname, datatype, dateformat. Description: Defines specific test data values, expected outcomes, database connections, and assertion logic used by datasets for Web scenario executions."
    ),
    Document(
        page_content="Table: dataset. Columns: datasetid(Primary Key), appid, baseline, createdby, createddate, datasetname(CRITICAL: Use this column when asked for the Test Case Name), isdefaultvalue, pageno, pageflowid, softdelete, deletedby, deleteddate, systemdataset, app_id, base_line, created_by, created_date, dataset_name, deleted_by, deleted_date, isdefault_value, page_no, pageflow_id, iscloned, validationflagatscan. Description: Represents a logical grouping of test data mapping to specific applications and UI page flows for Web scenario executions."
    ),
    Document(
        page_content="Table: scenariodataset. Columns: scdatasetid(Primary Key), createddate, isdeleted, scenariodatasetname, scenarioid, createdby, deletedby, deleteddate, iscloned. Description: Junction table linking test scenarios to their respective datasets and automation scripts for Web scenario executions."
    ),
    Document(
        page_content="Table: scenariodetails. Columns: id(Primary Key), baseline, created_by, created_date, isdeleted, pageflowid, pagesequence, scenarioid, version, deletedby, deleteddate. Description: Defines the step-by-step sequence of UI page flows or actions that make up a single test scenario for Web scenario executions."
    ),
    Document(
        page_content="Table: scenarios. Columns: scenarioid(Primary Key), appid, baseline, cloneid, createdby, createddate, isdeleted, scenarioname (This is the parent scenario wrapper. Do NOT use this for the specific Test Case Name), scenariosequence, custom, deletedby, deleteddate. Description: Master repository for individual test cases (scenarios) linked to specific applications related to Web scenario executions."
    ),
    Document(
        page_content="Table: scenariobatch. Columns: sc_batch_id(Primary Key), appid, baseline, batchname, createddate, createdby, deletedby, deleteddate, isdeleted, batchsequence, is_scenario_execution_parallel,abort. Description: Defines bundles (batches) of scenarios, allowing grouped and potentially parallel execution of tests in Web scenario executions."
    ),
    Document(
        page_content="Table: scenariobatchdata. Columns: scbatchdatid(Primary Key), createdby, createddate, deletedby, deleteddate, isdeleted, sc_batch_id, scenarioid, scenariobatchdataseq. Description: Maps which specific test scenarios are included inside a defined bundle or batch for Web scenario executions."
    ),
    Document(
        page_content="Table: scenariobatchdatasetdata. Columns: scbatchdatasetid(Primary Key), createdby, createddate, deletedby, deleteddate, isdeleted, sc_batch_id, scdatasetid, scenarioid, scbatchdatid, scenariobatchdatasetseq. Description: Specifies exactly which datasets are used for a scenario when it is executed within a specific bundle for Web scenario executions."
    ),
    Document(
        page_content="Table: aipageflow. Columns: aipageflowid(Primary Key), aipageflowreferenceid, appid, pagename, nextpagename, actionid, actionvalue, Imagename, screenshotname, screenchanges, baseline, created_by, created_date, isbaselinerequired, isdeleted, nextpageno, pageno, pending, screenshottime, version, deletedby, deleteddate, oldaipageflowid. Description: AI-augmented page flow for visual testing."
    ),
    Document(
        page_content="Table: pageflows. Columns: pageflowid(Primary Key), pageflowreferenceid, appid, pagename, nextpagename, actionid, actionvalue, recordingfilename, modelchanges, baseline, created_by, created_date, isbaselinerequired, isscenariosgenerated, isdeleted, nextpageno, pageno, recordingtime, version, isbusinessimpacted, createdby, createddate, deletedby, deleteddate, Modeid, Oldpageflowid. Description: recorded page flow steps."
    ),
    Document(
        page_content="Table: page_flows. Columns: page_flow_id(Primary Key), pageflow_reference_id, app_id, page_name, next_page_name, action_id, action_value, recording_file_name, model_changes, baseline, created_by, created_date, deleted_by, deleted_date, is_baseline_required, is_business_impacted, is_scenarios_generated, isdeleted, next_page_no, page_no, recording_time, version. Description: Modernized schema for recorded page flow steps."
    ),
    Document(
        page_content="Table: package_run_variables. Columns: Run_id(Primary Key), Variable_name, Rundetail_id, Var_value. Description: Stores dynamic runtime variables generated or passed during package executions."
    ),
    Document(
        page_content="Table: package_api_run_data. Columns: Packageapirundataid(Primary Key), Apirundataid, Apidatsequence, Duration, Executionendtime, Executionstarttime, Packagerundetailid, Result, Baseline. Description: Tracks high-level execution times, sequence, and final results specifically for API tests within a package."
    ),
    Document(
        page_content="Table: packageapirunvalidation. Columns: packageapirunvalidationid(Primary Key), actualvalue, apidatasetid, duration, executionendtime, executionstarttime, expectedvalue, result, packagerundetailid, Assert_type, count, packagedependentapirundetailid, assertid, dateformat, givenregex. Description: Contains detailed API validation checks, comparing expected versus actual payloads within package runs."
    ),
    Document(
        page_content="Table: packagedata. Columns: packagedata_id(Primary Key), apiid, api_name, app_id, createdby, createddate, deletedby, deleteddate, isdeleted, package_id, package_type, packagedatasequence, scenarioid, scenario_name, scenario_type, datasetappid, isactive, isunpicked, llmgenerated. Description: Defines the composition of a package, mapping the various API, Web, and PDF scenarios that belong to it."
    ),
    Document(
        page_content="Table: packagedatasetdata. Columns: packagedatasetid(Primary Key), apidatasetid, api_dataset_name, api_id, createdby, createddate, deletedby, deleteddate, isdeleted, package_id, packagedata_id, scdatasetid, scenario_dataset_name, scenarioid, isactive, isunpicked, llmgenerated. Description: Connects specific datasets to the APIs and scenarios mapped inside a package execution."
    ),
    Document(
        page_content="Table: packagedependent_api_run_detail. Columns: packagedependentapirundetailid(Primary Key), api_alias, api_id, api_name, data_set_alias, data_set_id, data_set_name, parent_api_id, parentapi_run_id, parent_data_set_id, request, response, result. Description: Stores information of chained or dependent API calls executed within a package."
    ),
    Document(
        page_content="Table: packagedetails. Columns: package_id(Primary Key), appid, baseline, createddate, createdby, Deletedby, deleteddate, environment_type, isdeleted, (Do NOT use this for the Test Case Name; it is only the wrapper), packagesequence, abort, isactive, llmgenerated. Description: Master table for package configurations, grouping Web, API, and PDF tests together into a single execution unit."
    ),
    Document(
        page_content="Table: packagereport. Columns: packageid, branch, branchcovered, branchmissed, complexity, complexitycovered, complexitymissed, instruction, instructioncovered, instructionmissed, lines, linescovered, linesmissed, methods, methodscovered, methodsmissed, Appid, baseline, classes, classescovered, classesmissed, packagename, reportname, runid. Description: Stores code coverage analytics and metrics generated after a full package run."
    ),
    Document(
        page_content="Table: packagerun. Columns: packagerunid(Primary Key), appid, browser, duration, envtype, executedby, executeddate, executionendtime, executionstarttime, result, store_value, abort, ispackageexecutionparallel, kill, executionruntime, template_name, deviceid, baseline (Used to filter versions. Find the latest by sorting 'executeddate' DESC). Description: Master record for a package execution instance tracking overall status, environment, and parallel execution flags."
    ),
    Document(
        page_content="Table: packagerundetail. Columns: packagerundetailid(Primary Key), apidatasetid, apiid, apirunsequence, baseline, duration, ismockingenabled, packageid, packagerunid, packagerunsequence, request, response, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), runsequence, scenariodatsetid, scenarioid, type, isdependentapi, executionendtime, executionstarttime, executionruntime, Deletedby, Deletedate, Isdeleted, Called_by. Description: Logs individual step-by-step executions (Web, API, PDF) within a package run, including payloads and mock settings."
    ),
    Document(
        page_content="Table: packagerunreport. Columns: packagerunreportid(Primary Key), createddate, packagerunid, report, reportstatus, runstatus. Description: Stores generated execution reports as byte arrays and their processing statuses for package runs."
    ),
    Document(
        page_content="Table: packagescenariorundata. Columns: packagescrundataid(Primary Key), datasetid, duration, executionendtime, executionstarttime, packagerundetailid, pageflowid, pagerunsequence, result, scenariodataid, executionruntime. Description: Captures page-level execution times data specifically for Web/PDF scenarios inside a package."
    ),
    Document(
        page_content="Table: packagesrundataassertiondetails. Columns: packagescrundataassertiondetailsid(Primary Key), actualvalue, asserttype, dataset_id, duration, elementsequence, element_type, elementlabel, executionendtime, executionstarttime, expectedvalue, inputvalue, message, packagerundetailid, packagescrundataid, pageflow_id, result, executionruntime, dateformat, errormessage. Description: Assertion and validation results comparing expected and actual values for Web/PDF scenarios within package executions."
    ),
    Document(
        page_content="Table: temppackagedata. Columns: packagedata_id, apiid, api_name, app_id, createdby, createddate, datasetappid, isactive, isunpicked, package_id, package_type, packagedatasequence, llmgenerated. Description: Temporary staging table used to hold configurations for APIs and scenarios while building a package."
    ),
    Document(
        page_content="Table: temppackagedataset. Columns: packagedatasetid, apidatasetid, api_dataset_name, api_id, createdby, createddate, isactive, isunpicked, package_id, packagedata_id, llmgenerated. Description: Temporary staging table used to link datasets to APIs and scenarios while a package is actively being built."
    ),
    Document(
        page_content="Table: temppackagedetails. Columns: pkgid, appid, baseline, createddate, createdby, isactive, packagename, packagesequence, llmgenerated. Description: Used as a temporary staging table for package details configuration."
    ),
    Document(
        page_content="Table: api_body. Columns: api_body_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, isdeleted, type, value, baseline, value_source. Description: Stores the raw payload, such as JSON, sent in the API request. Maps to the master API via api_id."
    ),
    Document(
        page_content="Table: api_data. Columns: api_data_id(Primary Key), api_body_id, api_data_set_id, api_id, api_parameter_id, created_by, created_date, deleted_by, deleted_date, isdeleted, value, baseline, param_source, body_source, raw_type, isjson_present, data_assist_doc_id, db_config_id, scriptnotion. Description: The core link connecting specific test data values to datasets, parameters, and API bodies. Tracks where the data is sourced from."
    ),
    Document(
        page_content="Table: api_data_set. Columns: api_data_set_id(Primary Key), api_id, app_id, assertionenabled, created_by, created_date, data_set_name, deleted_by, deleted_date, isdeleted, apitype, baseline, assertionid, expected_value, data_set_alias, api_data_set_alias, description, generate_type, bruledesc, bruleid, brdesc, brid, clonedfromid, iscloned, criteria. Description: Logical grouping defining a specific test case dataset, Contains expected outcomes and business rules for evaluating the API."
    ),
    Document(
        page_content="Table: api_details. Columns: api_id(Primary Key), api_name (CRITICAL: Use this column when asked for the Test Case Name. Do NOT use 'apiurl'), app_id, created_by, created_date, deleted_by, deleted_date, generate_type, isdeleted, method_type, url, apitype, baseline, is_baseline_required, api_alias, is_data_set_present, apisequence, schema_type, is_cloned_api, docname, method_name, protofile, refprotofile, request_name. Description: Master repository for every API. Defines the HTTP method, endpoint URL, schema type, and flags indicating if it was cloned or generated."
    ),
    Document(
        page_content="Table: api_header_details. Columns: header_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, header_name, header_value, isdeleted, baseline, header_source, db_config_id, data_assist_doc_id, headersourcetype, script_name. Description: Stores specific HTTP request headers, like Authorization or Content-Type, mapped directly to an API definition."
    ),
    Document(
        page_content="Table: api_parameter. Columns: api_parameter_id(Primary Key), api_id, created_by, created_date, deleted_by, deleted_date, isdeleted, issensitive, parameter_label, parameter_type, baseline, enumpresent, generatetype, parameterdatatype, required, swaggerconstraints, userconstraints, missing. Description: Defines specific URL components like query, path, and header parameters. Tracks data types, constraints, and sensitive data flags for API executions."
    ),
    Document(
        page_content="Table: api_schema. Columns: schema_id(Primary Key), input_ignore, input_schema, output_ignore, output_schema, baseline, deleted_by, deleted_date, isdeleted, api_id, created_by, created_date. Description: Stores the strict JSON structural contracts for an API to validate request and response formats independently of test data."
    ),
    Document(
        page_content="Table: api_schemas. Columns: schema_id, api_id, created_by, created_date, deleted_by, deleted_date, input_ignore, input_schema, isdeleted, output_ignore, output_schema, baseline, input_ignore_source, input_schema_source, output_ignore_source, output_schema_source, is_input_schema_file, is_output_schema_file, schemadetails, swaggerschema, swaggeroutputschema. Description: Extended schema definition table managing strict input/output structures, swagger definitions, and ignored schema fields for API execution."
    ),
    Document(
        page_content="Table: apiassertion. Columns: apiassertid(Primary Key), additionaldetails, apiasserttype, operator. Description: Defines validation types, which are then referred via assertionid in datasets for APIs."
    ),
    Document(
        page_content="Table: apidefaultvalue. Columns: id, arraydatatype, value, decimalplaces, digits, lowercase, maximumvalue, maxitems, maxlength, minimumvalue, minitems, minlength, spaces, specialchars, type, uppercase, apiid. Description: Stores fallback data generation rules and constraints for payload parameters when explicit test data is not provided for API execution."
    ),
    Document(
        page_content="Table: apirequestheaders. Columns: id(Primary Key), headername, headerdisplay_value. Description: A lookup or definition table storing standard HTTP header names and their display values for UI presentation in API execution."
    ),
    Document(
        page_content="Table: apirun. Columns: apirunid(Primary Key), apirundate, apiurl, appid, createdby, result, runtype, templatename, executionendtime, executionruntime, executionstarttime, kill, baseline (Used to filter versions. Find the latest by sorting 'apirundate' DESC). The master execution record for API tests. Description: Tracks overarching environments, URL run targets, execution durations, and final pass/fail results."
    ),
    Document(
        page_content="Table: apirundata. Columns: apirundataid(Primary Key), apidataid, apidatsequence, apirundetailid, baseline. Description: Sequence tracker that maps specific data inputs directly to the API run details during execution."
    ),
    Document(
        page_content="Table: apirundetail. Columns: apirundetailid(Primary Key), apidatasetid, apiid, apirunid, apirunsequence, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), response, request, actual_value, expected_value, is_mocking_enabled, baseline, dependent_api_webdto, is_dependent_api, standard_version, env_name, executionendtime, executionruntime, executionstarttime, specified_row, resdiffernce, hasparent, parentrundetailid, parenttype, grpcrunmode. Description: Log of a single API execution step. Captures raw HTTP traffic payloads, actual versus expected values, mocking flags, and specific error differences."
    ),
    Document(
        page_content="Table: apirunvalidation. Columns: apirunvalidationid(Primary Key), apidatasetid, result, actualvalue, expectedvalue, baseline, apirundetailid, dependent_api_run_detail_id, count, dateformat, givenregex, assertid, expectedresult, operator. Description: Logs the precise outcome of assertion checks during an API execution, showing why a test failed by comparing actual values to expected values and operators."
    ),
    Document(
        page_content="Table: apischema. Columns: schema_id, input_ignore, input_schema, output_ignore, output_schema, deleted_by, deleted_date, isdeleted, baseline. Description: Additional configuration table storing the structural JSON definitions expected for API request inputs and response outputs."
    ),
    Document(
        page_content="Table: apivalidation. Columns: apivalidationid(Primary Key), api_data_set_id, app_id, assertionid, created_by, created_date, deleted_by, deleted_date, expectedvalue, isdeleted, dbconfigid, operator, baseline, validation_source, count, dateformat, givenregex, db_driver, db_pwd, db_username, expectedresult, data_assist_doc_id, api_mapping_id. Description: Master definition for API dataset validations. Configures expected values, operators, and database connections required to validate an API response."
    ),
    Document(
        page_content="Table: pdfdataset. Columns: pdfdatasetid(Primary Key), createddate, createdby, datasetname, deletedby, isdeleted, pdffiledata, pdfid, zipfilename, temppdffiledata, baseline, isbaselined, filename. Description: Master container for a specific set of PDF test data, storing actual PDF dataset files or zip archives used during test execution."
    ),
    Document(
        page_content="Table: pdfdatasetdata. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldactualdata, fieldname, isdbquery, isdeleted, pdfdatasetid, pdffilename, pdfid, pdfsectionid, sectionname, row_validation, image, imagedata, baseline, source, dbname. Description: Maps specific fields within a PDF dataset to their expected text or image data, including flags for table-row validation."
    ),
    Document(
        page_content="Table: pdfexceldatasetdata. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldactualdata, fieldname, isdbquery, isdeleted, pdfdatasetid, pdffilename, pdfid, pdfsectionid, row_validation, sectionname, x1, x2, y1, y2, baseline, source. Description: Stores expected values and precise bounding box coordinates (x1, y1, x2, y2) for extracting and validating tabular or Excel-like data from PDFs."
    ),
    Document(
        page_content="Table: pdfrun. Columns: pdfrunid(Primary Key), appid, createdby, pdfrundate, result, runtype, kill, baseline (Used to filter versions. Find the latest by sorting 'pdfrundate' DESC). Description: The high-level master record for a PDF test execution, tracking the overall environment, run dates, and final pass/fail results."
    ),
    Document(
        page_content="Table: pdfrundata. Columns: pdfrundataid(Primary Key), actualvalue, dbid, expectedvalue, fieldname, fieldresult, isdbquery, pdfname, pdfrundetailid, sectionname, pdfsectionid, pdf_run_data, expectedfetchedvalue, assertid, isimage, baseline, source, dbname. Description: The execution log for PDF tests. Records the exact extracted actual values against expected values, database cross-checks, and field-level pass/fail results."
    ),
    Document(
        page_content="Table: pdfrundatadetail. Columns: pdfrundatadetailid(Primary Key), pdfdataid, pdfdatsequence, pdfrundetailid. Description: A sequence tracking table that records the exact order in which PDF data fields were processed during a test run."
    ),
    Document(
        page_content="Table: pdfrundetails. Columns: pdfrundetailid(Primary Key), appid, pdfdatasetid, pdfdatasetname, pdfid, pdfname, pdfrunid, result (CRITICAL Enum exact casing: 'pass', 'Terminated', 'Fail', 'NEW'), pdfrunsequence, pdftemplatename, dependent_api_webdto, baseline, envname. Description: Granular log tracking the execution of a specific PDF template within a larger run, linking the run to the specific dataset and environment."
    ),
    Document(
        page_content="Table: pdfsectiondetails. Columns: pdfsectionid(Primary Key), border, createddate, createdby, deletedby, is_dynamic_table, isdeleted, pdfid, pdfpageno, sectionname, sequence, isuserdefined, x1, x2, y1, y2, baseline. Description: Defines the blueprint of a PDF by chopping it into readable zones using exact coordinates and page numbers."
    ),
    Document(
        page_content="Table: pdftemplatedetails. Columns: pdfid(Primary Key), appid, createdatetime, createdby, deletedby, gridpdftemplatedata, isdeleted, name, originalpdftemplatedata, pdftemplatename (CRITICAL: Use this column when asked for the Test Case Name. Do NOT use 'pdfname')., updatedatetime, updatedby, tempgridpdftemplatedata, temporiginalpdftemplatedata, baseline, isbaselinerequired, isupdated. Description: Master repository for base PDF templates, storing the raw document binary data to serve as a visual baseline for comparisons."
    ),
    Document(
        page_content="Table: pdfvalidationdetails. Columns: id, assertid, createddate, createdby, dbid, deletedby, expectedvalue, fieldname, image, isdbquery, isdeleted, pdfid, pdfpageno, pdfsectionid, sectionname, x1, x2, y1, y2, imagedata, baseline, source, dbname. Description: The master rulebook for a PDF template. Defines bounding boxes, expected text or image values, and assertion operators for visual and data validation."
    )
]

schema_relationships = [
    ("run", "rundetail", "rundetail.runid(references) run.runid"),
    ("scenarios", "rundetail", "rundetail.scenarioid(references) scenarios.scenarioid"),
    ("dataset", "rundetail", "rundetail.scenariodatsetid(references) dataset.datasetid"),
    ("scenariobatch", "rundetail", "rundetail.batchid(references) scenariobatch.sc_batch_id"),
    ("rundetail", "rundata", "rundata.rundetailid(references) rundetail.rundetailid"),
    ("dataset", "rundata", "rundata.datasetid(references) dataset.datasetid"),
    ("data", "rundata", "rundata.scenariodataid(references) data.dataid"),
    ("rundata", "rundataasssertiondetails", "rundataasssertiondetails.rundataid(references) rundata.rundataid"),
    ("rundetail", "rundataasssertiondetails", "rundataasssertiondetails.run_detail_id(references) rundetail.rundetailid"),
    ("dataset", "rundataasssertiondetails", "rundataasssertiondetails.dataset_id(references) dataset.datasetid"),
    ("dataset", "data", "data.dataset_id(references) dataset.datasetid"),
    ("scenarios", "scenariodataset", "scenariodataset.scenarioid(references) scenarios.scenarioid"),
    ("scenarios", "scenariodetails", "scenariodetails.scenarioid(references) scenarios.scenarioid"),
    ("scenariobatch", "scenariobatchdata", "scenariobatchdata.sc_batch_id(references) scenariobatch.sc_batch_id"),
    ("scenarios", "scenariobatchdata", "scenariobatchdata.scenarioid(references) scenarios.scenarioid"),
    ("scenariobatch", "scenariobatchdatasetdata", "scenariobatchdatasetdata.sc_batch_id(references) scenariobatch.sc_batch_id"),
    ("scenariodataset", "scenariobatchdatasetdata", "scenariobatchdatasetdata.scdatasetid(references) scenariodataset.scdatasetid"),
    ("scenarios", "scenariobatchdatasetdata", "scenariobatchdatasetdata.scenarioid(references) scenarios.scenarioid"),
    ("run", "aipageflow", "aipageflow.appid = run.appid AND aipageflow.baseline = run.baseline"),
    ("run", "pageflow", "pageflow.appid = run.appid AND pageflow.baseline = run.baseline"),
    ("run", "page_flow", "page_flow.app_id = run.appid AND page_flow.baseline = run.baseline"),
    ("packagerundetail", "package_run_variables", "package_run_variables.Rundetail_id(references) packagerundetail.packagerundetailid"),
    ("packagerundetail", "package_api_run_data", "package_api_run_data.Packagerundetailid(references) packagerundetail.packagerundetailid"),
    ("packagerundetail", "packageapirunvalidation", "packageapirunvalidation.packagerundetailid(references) packagerundetail.packagerundetailid"),
    ("packagedependent_api_run_detail", "packageapirunvalidation", "packageapirunvalidation.packagedependentapirundetailid(references) packagedependent_api_run_detail.packagedependentapirundetailid"),
    ("packagedetails", "packagedata", "packagedata.package_id(references) packagedetails.package_id"),
    ("packagedata", "packagedatasetdata", "packagedatasetdata.packagedata_id(references) packagedata.packagedata_id"),
    ("packagedetails", "packagedatasetdata", "packagedatasetdata.package_id(references) packagedetails.package_id"),
    ("packagerundetail", "packagedependent_api_run_detail", "packagedependent_api_run_detail.parentapi_run_id(references) packagerundetail.packagerundetailid"),
    ("packagedetails", "packagereport", "packagereport.packageid(references) packagedetails.package_id"),
    ("packagerun", "packagereport", "packagereport.runid(references) packagerun.packagerunid"),
    ("packagerun", "packagerundetail", "packagerundetail.packagerunid(references) packagerun.packagerunid"),
    ("packagedetails", "packagerundetail", "packagerundetail.packageid(references) packagedetails.package_id"),
    ("packagerun", "packagerunreport", "packagerunreport.packagerunid(references) packagerun.packagerunid"),
    ("packagerundetail", "packagescenariorundata", "packagescenariorundata.packagerundetailid(references) packagerundetail.packagerundetailid"),
    ("packagerundetail", "packagesrundataassertiondetails", "packagesrundataassertiondetails.packagerundetailid(references) packagerundetail.packagerundetailid"),
    ("packagescenariorundata", "packagesrundataassertiondetails", "packagesrundataassertiondetails.packagescrundataid(references) packagescenariorundata.packagescrundataid"),
    ("temppackagedetails", "temppackagedata", "temppackagedata.package_id(references) temppackagedetails.pkgid"),
    ("temppackagedetails", "temppackagedataset", "temppackagedataset.package_id(references) temppackagedetails.pkgid"),
    ("temppackagedata", "temppackagedataset", "temppackagedataset.packagedata_id(references) temppackagedata.packagedata_id"),
    ("api_details", "api_body", "api_body.api_id(references) api_details.api_id"),
    ("api_details", "api_data", "api_data.api_id(references) api_details.api_id"),
    ("api_body", "api_data", "api_data.api_body_id(references) api_body.api_body_id"),
    ("api_data_set", "api_data", "api_data.api_data_set_id(references) api_data_set.api_data_set_id"),
    ("api_parameter", "api_data", "api_data.api_parameter_id(references) api_parameter.api_parameter_id"),
    ("api_details", "api_data_set", "api_data_set.api_id(references) api_details.api_id"),
    ("apiassertion", "api_data_set", "api_data_set.assertionid(references) apiassertion.apiassertid"),
    ("api_details", "api_header_details", "api_header_details.api_id(references) api_details.api_id"),
    ("api_details", "api_parameter", "api_parameter.api_id(references) api_details.api_id"),
    ("api_details", "api_schema", "api_schema.api_id(references) api_details.api_id"),
    ("api_details", "api_schemas", "api_schemas.api_id(references) api_details.api_id"),
    ("api_details", "apidefaultvalue", "apidefaultvalue.apiid(references) api_details.api_id"),
    ("apirundetail", "apirundata", "apirundata.apirundetailid(references) apirundetail.apirundetailid"),
    ("api_data", "apirundata", "apirundata.apidataid(references) api_data.api_data_id"),
    ("apirun", "apirundetail", "apirundetail.apirunid(references) apirun.apirunid"),
    ("api_details", "apirundetail", "apirundetail.apiid(references) api_details.api_id"),
    ("api_data_set", "apirundetail", "apirundetail.apidatasetid(references) api_data_set.api_data_set_id"),
    ("apirundetail", "apirunvalidation", "apirunvalidation.apirundetailid(references) apirundetail.apirundetailid"),
    ("api_data_set", "apirunvalidation", "apirunvalidation.apidatasetid(references) api_data_set.api_data_set_id"),
    ("apiassertion", "apirunvalidation", "apirunvalidation.assertid(references) apiassertion.apiassertid"),
    ("apirundetail", "apirunvalidation", "apirunvalidation.dependent_api_run_detail_id(references) apirundetail.apirundetailid"),
    ("api_data_set", "apivalidation", "apivalidation.api_data_set_id(references) api_data_set.api_data_set_id"),
    ("apiassertion", "apivalidation", "apivalidation.assertionid(references) apiassertion.apiassertid"),
    ("pdftemplatedetails", "pdfdataset", "pdfdataset.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdfdataset", "pdfdatasetdata", "pdfdatasetdata.pdfdatasetid(references) pdfdataset.pdfdatasetid"),
    ("pdftemplatedetails", "pdfdatasetdata", "pdfdatasetdata.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdfsectiondetails", "pdfdatasetdata", "pdfdatasetdata.pdfsectionid(references) pdfsectiondetails.pdfsectionid"),
    ("pdfdataset", "pdfexceldatasetdata", "pdfexceldatasetdata.pdfdatasetid(references) pdfdataset.pdfdatasetid"),
    ("pdftemplatedetails", "pdfexceldatasetdata", "pdfexceldatasetdata.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdfsectiondetails", "pdfexceldatasetdata", "pdfexceldatasetdata.pdfsectionid(references) pdfsectiondetails.pdfsectionid"),
    ("pdfrundetails", "pdfrundata", "pdfrundata.pdfrundetailid(references) pdfrundetails.pdfrundetailid"),
    ("pdfsectiondetails", "pdfrundata", "pdfrundata.pdfsectionid(references) pdfsectiondetails.pdfsectionid"),
    ("pdfrundetails", "pdfrundatadetail", "pdfrundatadetail.pdfrundetailid(references) pdfrundetails.pdfrundetailid"),
    ("pdfrun", "pdfrundetails", "pdfrundetails.pdfrunid(references) pdfrun.pdfrunid"),
    ("pdftemplatedetails", "pdfrundetails", "pdfrundetails.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdfdataset", "pdfrundetails", "pdfrundetails.pdfdatasetid(references) pdfdataset.pdfdatasetid"),
    ("pdftemplatedetails", "pdfsectiondetails", "pdfsectiondetails.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdftemplatedetails", "pdfvalidationdetails", "pdfvalidationdetails.pdfid(references) pdftemplatedetails.pdfid"),
    ("pdfsectiondetails", "pdfvalidationdetails", "pdfvalidationdetails.pdfsectionid(references) pdfsectiondetails.pdfsectionid")
]


from langchain_core.documents import Document

sample_query_docs = [
    # ==========================================
    # INTENT 1: Consistently Failing Test Cases
    # ==========================================
    Document(
        page_content="DOMAIN: WEB. INTENT: Consistently Failing Test Cases (Last 15 Runs). GOAL: Identify unstable/flaky test cases by finding ones that failed more than 2 times in the last 15 executions.",
        metadata={"domain": "web", "sql": """WITH Last15WebRuns AS (
    SELECT runid FROM run WHERE appid = 43920660 ORDER BY rundate DESC LIMIT 15
),
ConsistentFailures AS (
    SELECT scenariodatsetid
    FROM rundetail
    WHERE runid IN (SELECT runid FROM Last15WebRuns) AND result = 'Fail'
    GROUP BY scenariodatsetid
    HAVING COUNT(rundetailid) > 2
)
SELECT 
    'WEB' AS Execution_Domain, 
    d.datasetname AS Test_Case_Name, 
    r.*, 
    rd.*
FROM rundetail rd
LEFT JOIN dataset d ON rd.scenariodatsetid = d.datasetid
LEFT JOIN run r ON rd.runid = r.runid
WHERE rd.runid IN (SELECT runid FROM Last15WebRuns) 
  AND rd.result = 'Fail'
  AND rd.scenariodatsetid IN (SELECT scenariodatsetid FROM ConsistentFailures);"""}
    ),
    
    Document(
        page_content="DOMAIN: API. INTENT: Consistently Failing Test Cases (Last 15 Runs). GOAL: Identify unstable/flaky test cases by finding ones that failed more than 2 times in the last 15 executions.",
        metadata={"domain": "api", "sql": """WITH Last15ApiRuns AS (
    SELECT apirunid FROM apirun WHERE appid = 1032110 ORDER BY apirundate DESC LIMIT 15
),
ConsistentFailures AS (
    SELECT apiid
    FROM apirundetail
    WHERE apirunid IN (SELECT apirunid FROM Last15ApiRuns) AND result = 'Fail'
    GROUP BY apiid
    HAVING COUNT(apirundetailid) > 2
)
SELECT 
    'API' AS Execution_Domain, 
    ad.api_name AS Test_Case_Name, 
    ar.*, 
    ard.*
FROM apirundetail ard
LEFT JOIN api_details ad ON ard.apiid = ad.api_id
LEFT JOIN apirun ar ON ard.apirunid = ar.apirunid
WHERE ard.apirunid IN (SELECT apirunid FROM Last15ApiRuns) 
  AND ard.result = 'Fail'
  AND ard.apiid IN (SELECT apiid FROM ConsistentFailures);"""}
    ),

    Document(
        page_content="DOMAIN: PDF. INTENT: Consistently Failing Test Cases (Last 15 Runs). GOAL: Identify unstable/flaky test cases by finding ones that failed more than 2 times in the last 15 executions.",
        metadata={"domain": "pdf", "sql": """WITH Last15PdfRuns AS (
    SELECT pdfrunid FROM pdfrun WHERE appid = 43920715 ORDER BY pdfrundate DESC LIMIT 15
),
ConsistentFailures AS (
    SELECT pdfid
    FROM pdfrundetails
    WHERE pdfrunid IN (SELECT pdfrunid FROM Last15PdfRuns) AND result = 'Fail'
    GROUP BY pdfid
    HAVING COUNT(pdfrundetailid) > 2
)
SELECT 
    'PDF' AS Execution_Domain, 
    ptd.pdftemplatename AS Test_Case_Name, 
    pr.*, 
    prd.*
FROM pdfrundetails prd
LEFT JOIN pdftemplatedetails ptd ON prd.pdfid = ptd.pdfid
LEFT JOIN pdfrun pr ON prd.pdfrunid = pr.pdfrunid
WHERE prd.pdfrunid IN (SELECT pdfrunid FROM Last15PdfRuns) 
  AND prd.result = 'Fail'
  AND prd.pdfid IN (SELECT pdfid FROM ConsistentFailures);"""}
    ),

    Document(
        page_content="DOMAIN: PACKAGE. INTENT: Consistently Failing Test Cases (Last 15 Runs). GOAL: Identify unstable/flaky test cases by finding ones that failed more than 2 times in the last 15 executions.",
        metadata={"domain": "package", "sql": """WITH Last15PackageRuns AS (
    SELECT packagerunid FROM packagerun WHERE appid = 43920721 ORDER BY executeddate DESC LIMIT 15
),
ConsistentFailures AS (
    SELECT CASE WHEN type='api' THEN apiid ELSE scenarioid END AS entityId
    FROM packagerundetail
    WHERE packagerunid IN (SELECT packagerunid FROM Last15PackageRuns) AND result='Fail'
    GROUP BY CASE WHEN type='api' THEN apiid ELSE scenarioid END
    HAVING COUNT(packagerundetailid) > 2
)
SELECT 'PACKAGE' AS Execution_Domain,
       CASE WHEN prd.type='api' THEN pd.api_name ELSE pd.scenario_name END AS Test_Case_Name,
       prun.*, prd.*
FROM packagerundetail prd
LEFT JOIN packagedata pd ON ((prd.type='api' AND prd.apiid=pd.apiid) OR (prd.type='scenario' AND prd.scenarioid=pd.scenarioid))
LEFT JOIN packagerun prun ON prd.packagerunid=prun.packagerunid
WHERE prd.packagerunid IN (SELECT packagerunid FROM Last15PackageRuns)
  AND prd.result='Fail'
  AND ((prd.type='api' AND prd.apiid IN (SELECT entityId FROM ConsistentFailures))
    OR (prd.type='scenario' AND prd.scenarioid IN (SELECT entityId FROM ConsistentFailures)));"""}
    ),

    # ==========================================
    # INTENT 2: Features/Screens/Endpoints with Highest Failures
    # ==========================================
    Document(
        page_content="DOMAIN: WEB. INTENT: Features/Screens/Endpoints with Highest Failures (Last 15 Runs). GOAL: Dive deeper than the test-case level to pinpoint the exact UI Screen (pageflow), API Endpoint (url), or PDF Field (pdfsectiondetails) causing the most breaks. Extract step-by-step detail rows.",
        metadata={"domain": "web", "sql": """WITH Last15WebRuns AS (
    SELECT runid FROM run where appid= 43920660 ORDER BY rundate DESC LIMIT 15
),
HighFailureScreens AS (
    SELECT pageflowid
    FROM rundata
    WHERE rundetailid IN (SELECT rundetailid FROM rundetail WHERE runid IN (SELECT runid FROM Last15WebRuns))
      AND result = 'Fail'
    GROUP BY pageflowid
    HAVING COUNT(rundataid) > 2
)
SELECT 
    'WEB' AS Execution_Domain, 
    pf.pagename AS Failing_Screen_Name, 
    r.*, 
    rd.*, 
    rdata.*
FROM rundata rdata
LEFT JOIN pageflows pf ON rdata.pageflowid = pf.pageflowid
LEFT JOIN rundetail rd ON rdata.rundetailid = rd.rundetailid
LEFT JOIN run r ON rd.runid = r.runid
WHERE rdata.rundetailid IN (SELECT rundetailid FROM rundetail WHERE runid IN (SELECT runid FROM Last15WebRuns))
  AND rdata.result = 'Fail'
  AND rdata.pageflowid IN (SELECT pageflowid FROM HighFailureScreens);"""}
    ),

    Document(
        page_content="DOMAIN: API. INTENT: Features/Screens/Endpoints with Highest Failures (Last 15 Runs). GOAL: Dive deeper than the test-case level to pinpoint the exact UI Screen (pageflow), API Endpoint (url), or PDF Field (pdfsectiondetails) causing the most breaks. Extract step-by-step detail rows.",
        metadata={"domain": "api", "sql": """WITH Last15ApiRuns AS (
    SELECT apirunid FROM apirun where appid = 1032110 ORDER BY apirundate DESC LIMIT 15
),
HighFailureEndpoints AS (
    SELECT apiid
    FROM apirundetail
    WHERE apirunid IN (SELECT apirunid FROM Last15ApiRuns) AND result = 'Fail'
    GROUP BY apiid
    HAVING COUNT(apirundetailid) > 2
)
SELECT 
    'API' AS Execution_Domain, 
    ad.url AS Failing_Endpoint, 
    ar.*, 
    ard.*
FROM apirundetail ard
LEFT JOIN api_details ad ON ard.apiid = ad.api_id
LEFT JOIN apirun ar ON ard.apirunid = ar.apirunid
WHERE ard.apirunid IN (SELECT apirunid FROM Last15ApiRuns) 
  AND ard.result = 'Fail'
  AND ard.apiid IN (SELECT apiid FROM HighFailureEndpoints);"""}
    ),

    Document(
        page_content="DOMAIN: PDF. INTENT: Features/Screens/Endpoints with Highest Failures (Last 15 Runs). GOAL: Dive deeper than the test-case level to pinpoint the exact UI Screen (pageflow), API Endpoint (url), or PDF Field (pdfsectiondetails) causing the most breaks. Extract step-by-step detail rows.",
        metadata={"domain": "pdf", "sql": """WITH Last15PdfRuns AS (
    SELECT pdfrunid FROM pdfrun WHERE appid = 43920715 ORDER BY pdfrundate DESC LIMIT 15
),
HighFailureSections AS (
    SELECT pdfsectionid
    FROM pdfrundata
    WHERE pdfrundetailid IN (SELECT pdfrundetailid FROM pdfrundetails WHERE pdfrunid IN (SELECT pdfrunid FROM Last15PdfRuns))
      AND fieldresult = 'Fail'
    GROUP BY pdfsectionid
    HAVING COUNT(pdfrundataid) > 2
)
SELECT 
    'PDF' AS Execution_Domain, 
    psd.sectionname AS Failing_PDF_Section, 
    pr.*, 
    prd.*, 
    pdata.*
FROM pdfrundata pdata
LEFT JOIN pdfsectiondetails psd ON pdata.pdfsectionid = psd.pdfsectionid
LEFT JOIN pdfrundetails prd ON pdata.pdfrundetailid = prd.pdfrundetailid
LEFT JOIN pdfrun pr ON prd.pdfrunid = pr.pdfrunid
WHERE pdata.pdfrundetailid IN (SELECT pdfrundetailid FROM pdfrundetails WHERE pdfrunid IN (SELECT pdfrunid FROM Last15PdfRuns))
  AND pdata.fieldresult = 'Fail'
  AND pdata.pdfsectionid IN (SELECT pdfsectionid FROM HighFailureSections);"""}
    ),

    Document(
        page_content="DOMAIN: PACKAGE. INTENT: Features/Screens/Endpoints with Highest Failures (Last 15 Runs). GOAL: Dive deeper than the test-case level to pinpoint the exact UI Screen (pageflow), API Endpoint (url), or PDF Field (pdfsectiondetails) causing the most breaks. Extract step-by-step detail rows.",
        metadata={"domain": "package", "sql": """WITH Last15 AS (
    SELECT packagerunid FROM packagerun WHERE appid=43920721 ORDER BY executeddate DESC LIMIT 15
),
HighFailureScreens AS (SELECT pageflowid FROM packagescenariorundata WHERE packagerundetailid IN (SELECT packagerundetailid FROM packagerundetail WHERE packagerunid IN (SELECT packagerunid FROM Last15)) AND result='Fail' GROUP BY pageflowid HAVING COUNT(packagescrundataid)>2),
HighFailureApiSteps AS (SELECT apidataid FROM packageapirundata WHERE packagerundetailid IN (SELECT packagerundetailid FROM packagerundetail WHERE packagerunid IN (SELECT packagerunid FROM Last15)) AND result='Fail' GROUP BY apidataid HAVING COUNT(packageapirundataid)>2)

-- SCREENS
SELECT 
    'PACKAGE' AS Execution_Domain,'SCREEN' AS Failure_Type,pf.pagename AS Failing_Name,
    prun.packagerunid,prun.executeddate,
    prd.packagerundetailid,prd.type,prd.scenarioid,prd.apiid,prd.result AS detail_result,
    psrd.pageflowid AS step_id,psrd.result AS step_result,psrd.executionstarttime,psrd.executionendtime,psrd.duration
FROM packagescenariorundata psrd
LEFT JOIN pageflows pf ON psrd.pageflowid=pf.pageflowid
LEFT JOIN packagerundetail prd ON psrd.packagerundetailid=prd.packagerundetailid
LEFT JOIN packagerun prun ON prd.packagerunid=prun.packagerunid
WHERE psrd.result='Fail' AND psrd.pageflowid IN (SELECT pageflowid FROM HighFailureScreens)

UNION ALL

-- APIS
SELECT 
    'PACKAGE' AS Execution_Domain,'API' AS Failure_Type,pd.api_name AS Failing_Name,
    prun.packagerunid,prun.executeddate,
    prd.packagerundetailid,prd.type,prd.scenarioid,prd.apiid,prd.result AS detail_result,
    pard.apidataid AS step_id,pard.result AS step_result,pard.executionstarttime,pard.executionendtime,pard.duration
FROM packageapirundata pard
LEFT JOIN packagerundetail prd ON pard.packagerundetailid=prd.packagerundetailid
LEFT JOIN packagedata pd ON prd.apiid=pd.apiid
LEFT JOIN packagerun prun ON prd.packagerunid=prun.packagerunid
WHERE pard.result='Fail' AND pard.apidataid IN (SELECT apidataid FROM HighFailureApiSteps);"""}
    ),

    # ==========================================
    # INTENT 3: Failures Blocking Downstream Testing
    # ==========================================
    Document(
        page_content="DOMAIN: WEB. INTENT: Failures Blocking Downstream Testing. GOAL: Find failed tests acting as dependencies for other tests (bottlenecks). Time thresholds are excluded to find all historical root blockers.",
        metadata={"domain": "web", "sql": """SELECT 
    'WEB' AS Execution_Domain, 
    d.datasetname AS Blocking_Web_Test_Case, 
    r.*, 
    rd.*
FROM rundetail rd
LEFT JOIN dataset d ON rd.scenariodatsetid = d.datasetid
LEFT JOIN run r ON rd.runid = r.runid
WHERE rd.result = 'Fail' 
  AND rd.is_dependent = true
  AND rd.runid IN (SELECT runid FROM run WHERE appid = 43920660);"""}
    ),

    Document(
        page_content="DOMAIN: API. INTENT: Failures Blocking Downstream Testing. GOAL: Find failed tests acting as dependencies for other tests (bottlenecks). Time thresholds are excluded to find all historical root blockers.",
        metadata={"domain": "api", "sql": """SELECT 
    'API' AS Execution_Domain, 
    ad.api_name AS Blocking_API_Test_Case, 
    ar.*, 
    ard.*
FROM apirundetail ard
LEFT JOIN api_details ad ON ard.apiid = ad.api_id
LEFT JOIN apirun ar ON ard.apirunid = ar.apirunid
WHERE ard.result = 'Fail' 
  AND (ard.hasparent = true OR ard.parentrundetailid IS NOT NULL)
  AND ard.apirunid IN (SELECT apirunid FROM apirun WHERE appid = 43807333);"""}
    ),

    Document(
        page_content="DOMAIN: PDF. INTENT: Failures Blocking Downstream Testing. GOAL: Find failed tests acting as dependencies for other tests (bottlenecks). Time thresholds are excluded to find all historical root blockers.",
        metadata={"domain": "pdf", "sql": """SELECT 
    'PDF' AS Execution_Domain, 
    ptd.pdftemplatename AS Blocking_PDF_Test_Case, 
    pr.*, 
    prd.*
FROM pdfrundetails prd
LEFT JOIN pdftemplatedetails ptd ON prd.pdfid = ptd.pdfid
LEFT JOIN pdfrun pr ON prd.pdfrunid = pr.pdfrunid
WHERE prd.result = 'Fail' 
  AND prd.dependent_api_webdto IS NOT NULL
  AND prd.pdfrunid IN (SELECT pdfrunid FROM pdfrun WHERE appid = 43920715);"""}
    ),

    Document(
        page_content="DOMAIN: PACKAGE. INTENT: Failures Blocking Downstream Testing. GOAL: Find failed tests acting as dependencies for other tests (bottlenecks). Time thresholds are excluded to find all historical root blockers.",
        metadata={"domain": "package", "sql": """SELECT 
    'PACKAGE' AS Execution_Domain, 
    CASE 
        WHEN prd.type = 'scenario' THEN pd.scenario_name
        WHEN prd.type = 'api' THEN pd.api_name
    END AS Blocking_Package_Test_Case,
    prun.*, 
    prd.*
FROM packagerundetail prd
LEFT JOIN packagedata pd 
       ON (prd.type = 'scenario' AND prd.scenarioid = pd.scenarioid)
       OR (prd.type = 'api' AND prd.apiid = pd.apiid)
LEFT JOIN packagerun prun ON prd.packagerunid = prun.packagerunid
WHERE prd.result = 'Fail' 
  AND prd.Called_by IS NOT NULL 
  AND prd.packagerunid IN (SELECT packagerunid FROM packagerun WHERE appid = 43920721);"""}
    )
]