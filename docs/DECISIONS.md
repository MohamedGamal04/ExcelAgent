# DECISIONS

## Architecture
- Used a CLI-first architecture because the task emphasizes practical natural-language querying over spreadsheets.
- Chose a modular `src/queryquest` package structure to separate concerns: CLI, setup/state, chat orchestration, Excel context, and SQL execution.
- Implemented a custom tool layer end-to-end (no LangChain/LlamaIndex/AutoGen/CrewAI), in line with task constraints.
- Used DuckDB as the query engine over pandas DataFrames registered from Excel files for fast local SQL execution.

## LLM integration
- Used OpenAI-compatible chat completions to support multiple free/local providers behind a consistent interface.
- Added interactive setup for provider/model/API key selection and persisted state in `.provider.json`.
- Kept provider configuration centralized in `config.py` for easier provider/model changes.

## Excel handling
- Built Excel context tooling to summarize sheets, dtypes, min/max, row counts, and sample rows for the system prompt.
- Registered both original and normalized table names to make model-generated SQL more resilient to spaces/special characters.
- Preserved write-back support for DML with explicit user confirmation before saving changes to workbook files.
- Added table previews for SQL statements and query results, including bounded JOIN previews.

## Tradeoffs
- The current execution flow uses the first sheet of each workbook as the active SQL table and write-back target.
- SQL extraction depends on model output structure; robustness is improved by parsing fenced and embedded JSON, but fully malformed responses still fail safely.
- The executor is intentionally centralized in one module for delivery speed, at the cost of larger function scope.
- Interactive CLI UX is prioritized over API/server deployment for this task.

## Testing
- Added baseline unit tests using `unittest` (no extra test framework dependency):
	- `tests/test_cli.py`
	- `tests/test_sql_handoff.py`
	- `tests/test_state.py`
- Test focus is core reliability: argument handling, SQL JSON extraction resilience, and persisted state behavior.

## What I would do differently next
- Split `sql/executor.py` into smaller components (table registration, statement execution, write-back strategy).
- Add integration tests for Excel round-trips and DML write-back correctness across multi-sheet workbooks.
- Add stricter schema-aware safeguards before executing destructive statements.
- Add structured error objects for user-facing explanations when SQL parsing/execution fails.
