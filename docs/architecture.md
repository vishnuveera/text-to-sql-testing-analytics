# Architecture

## High-Level Workflow

```mermaid
flowchart TD
    A[User Question]
    B[Intent Validation]
    C[Testing Domain Selection]
    D[Intent Refinement]
    E[SQL Generation]
    F[Database Execution]
    G{Execution Successful?}
    H[Retry / SQL Correction]
    I[Result Analysis]
    J[Final Answer]

    A --> B --> C --> D --> E --> F --> G
    G -- No --> H --> E
    G -- Yes --> I --> J
```

## Components

### Orchestrator
Coordinates the application's workflow and domain-level processing.

### Intent Validation and Refinement
Checks whether a question is supported and converts it into a more focused intent.

### SQL Generation
Uses LLM prompts and schema context to generate SQL for the requested analytics task.

### Database Executor
Executes generated queries and provides a retry/self-healing path for failures.

### Result Analysis
Interprets retrieved data to prepare a response relevant to the original question.

## Limitations

This diagram represents the intended high-level processing flow. Actual
runtime behavior and security controls should be validated against the
published implementation.