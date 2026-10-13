# Text-to-SQL Testing Analytics Agent

An LLM-powered application that translates natural-language questions about test execution analytics into SQL queries, retrieves data from a database, and summarizes relevant results.

## Project Overview

The application uses an orchestrated workflow to validate user intent, identify relevant testing domains, refine queries, generate SQL, execute database queries, and analyze the returned results.

## Intended Workflow

1. Collect a natural-language analytics question.
2. Validate whether the request is within the supported testing analytics scope.
3. Identify the relevant testing domain or domains.
4. Refine the request into a focused intent.
5. Generate SQL using LLM prompts and database-schema context.
6. Execute the generated query.
7. Attempt query correction when execution fails.
8. Analyze the retrieved data and prepare a user-facing result.

## Technology Stack

- Python
- LangChain
- Azure OpenAI integration
- PostgreSQL
- Chroma-based retrieval
- Concurrent processing

## Repository Structure

- `src/text_to_sql_analytics/` — application modules
- `config/` — example configuration templates
- `docs/` — architecture documentation
- `examples/` — synthetic demonstration questions
- `tests/` — automated tests

## Security and Data Handling

Only use database connections and schemas that you are authorized to access. Generated SQL must be validated before execution, and database credentials must never be committed.

## Project Status

Portfolio preparation in progress. End-to-end execution, reproducibility, and security controls must be verified before this project is described as production-ready.