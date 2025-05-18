# Day-Summary & Action-Hub

This project summarises daily transcripts, extracts actionable tasks, and saves them to Notion and Todoist. It provides a Streamlit interface and CLI for automation. It relies on the [OpenAI Python library](https://github.com/openai/openai-python). If the library isn't installed the OpenAI features will be disabled.

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
   The `--model` flag selects the OpenAI model used for summarisation. When
   `best_reasoning` is supplied, the app queries OpenAI for the model tagged with
   the best reasoning capability and caches that ID for 24 hours.

## Tests
Run unit tests with:
```bash
make test
```

