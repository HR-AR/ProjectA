# Day-Summary & Action-Hub

This project summarises daily transcripts, extracts actionable tasks, and saves them to Notion and Todoist. It provides a Streamlit interface and CLI for automation.

## Setup
1. Create a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in API keys.
4. Run the app:
   ```bash
   make run -- --model best_reasoning
   ```

## CLI usage
`app.py` accepts optional flags:
- `--date YYYY-MM-DD` pull transcript for the given date (defaults to yesterday)
- `--file PATH` read transcript from file or `-` for stdin
- `--model MODEL_ID|best_reasoning` choose OpenAI model
- `--max-retries N` override retry count

## Tests
Run unit tests with:
```bash
make test
```
