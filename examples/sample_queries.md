# Sample Natural-Language Queries

This document contains example questions for the Text-to-SQL Testing Analytics Agent.

The agent is designed to interpret natural-language requests about previously executed tests, generate SQL using available schema context, retrieve relevant records, and summarize the results.

**Note:** These are sample inputs, not guaranteed SQL outputs. The actual generated SQL depends on the configured schema, database context, and available data.

## 1. Web Testing Analytics

### Failed test executions
> Give me a report of failed Web test executions in the latest baseline.

Expected focus: failed execution records associated with the requested baseline.

### Repeated failures
> Identify the Web test cases that failed most often in the last 10 runs.

Expected focus: repeated failures grouped by test case and limited to the requested execution history.

### Page-level failures
> Which Web application pages have the highest number of failures?

Expected focus: identifying pages associated with failed Web test executions.

### Execution history
> Show the execution history of Web test cases over the last 7 days.

Expected focus: execution outcomes within the requested time period.

## 2. API Testing Analytics

### Failed API executions
> Retrieve failed API test executions in the latest baseline.

Expected focus: failed API execution records.

### API failure analysis
> Which API endpoints have the most failed test executions?

Expected focus: identifying frequently failing API tests or endpoints where the required schema information is available.

### Execution duration
> Show the slowest API test cases and their execution durations.

Expected focus: comparing execution durations using available timing fields.

### Historical comparison
> Compare API test failures across the last 5 runs.

Expected focus: comparing failure counts across the selected execution history.

## 3. PDF Testing Analytics

### Failed PDF validations
> Summarize failed PDF template validations in the latest baseline.

Expected focus: failed PDF validation records.

### Failure trends
> Identify PDF templates with the most failures during the last 30 days.

Expected focus: grouping available PDF failure records by template and time period.

### Historical failures
> Show the history of failed PDF test executions for a selected time period.

Expected focus: retrieving historical failures within the requested dates.

## 4. Package Testing Analytics

### Failed package executions
> Give me a report of failed test cases in the latest test package execution.

Expected focus: package execution results and relevant test case details.

### Repeated package failures
> Identify package test cases that fail repeatedly over the last 10 runs.

Expected focus: recurring failures within package execution history.

### Package execution details
> Show the execution results and durations of test cases within a package.

Expected focus: package execution outcomes and available timing information.

## 5. Cross-Domain Analytics

### Overall failure summary
> Summarize failed test executions across Web, API, PDF, and Package testing.

Expected focus: separate, domain-specific queries followed by a consolidated summary when supported by the application workflow.

### Domain comparison
> Compare the number of failures across Web, API, PDF, and Package testing for the latest baseline.

Expected focus: comparing domain-level metrics without assuming that unrelated testing-domain tables can be joined.

## 6. Query Refinement Examples

The following questions demonstrate cases where additional context may be required.

**Ambiguous timeframe**

> Show failed test cases.

Potential clarification: Which timeframe or execution baseline should be considered?

**Ambiguous workspace**

> Show the latest test execution report.

Potential clarification: Which workspace or application should be used?

**Unsupported request**

> Write a Python script to create automated UI tests.

Expected behavior: The request should be rejected because the agent is intended for analytics on existing test executions, not code generation or new test execution.

## 7. Expected Processing Workflow

For an eligible analytics request, the intended workflow is:

1. Validate the user's intent.
2. Determine the relevant testing domain or domains.
3. Refine the request while retaining applicable filters.
4. Retrieve relevant schema context.
5. Generate a SQL query for the selected domain.
6. Execute the query against the authorized database.
7. Attempt correction when execution fails, subject to the configured retry limit.
8. Analyze the returned records and prepare a user-facing answer.

## 8. Important Limitations

- Query results depend on the available schema and database records.
- The examples do not guarantee a specific SQL statement or result.
- Generated SQL must be validated before execution.
- Cross-domain reporting must respect domain-specific query constraints.
- This document contains example user requests, not production database records or customer data.