import argparse
import datetime as dt
import os
import sys
from pathlib import Path

import streamlit as st

from config import get_model
from llm import summarise, classify
from notion_client import NotionClient
from todoist_client import TodoistClient
from limitless_client import LimitlessClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Day-Summary & Action-Hub")
    parser.add_argument("--date", type=str, default=None,
                        help="YYYY-MM-DD of transcript; defaults to yesterday")
    parser.add_argument("--model", type=str, default=os.getenv("OPENAI_DEFAULT_MODEL"),
                        help="Model ID or best_reasoning")
    parser.add_argument("--max-retries", type=int,
                        default=int(os.getenv("OPENAI_MAX_RETRIES", "6")),
                        help="OpenAI max retries")
    return parser.parse_args()


def load_transcript(limitless: LimitlessClient, date: str | None) -> str:
    if date is None:
        tz = dt.timezone(dt.timedelta(hours=-5))  # America/Chicago offset
        date = (dt.datetime.now(tz) - dt.timedelta(days=1)).date().isoformat()
    return limitless.get_transcript(date)


def main(transcript: str, model: str, max_retries: int) -> None:
    narrative, tasks = summarise(transcript, model=model, max_retries=max_retries)
    classified = classify(tasks)

    notion = NotionClient()
    todoist = TodoistClient()
    notion.save_day(narrative, tasks, classified)

    st.title("Day-Summary & Action-Hub")
    left, right = st.columns(2)
    with left:
        st.subheader("Narrative")
        st.write(narrative)
    with right:
        st.subheader("Tasks")
        for section, items in classified.items():
            with st.expander(section.title() + " Tasks"):
                for item in items:
                    if st.button(f"Send: {item}"):
                        success = todoist.add_task(item)
                        if success:
                            st.toast("✅ Sent", icon="✅")
                        else:
                            st.toast("🚦 Still rate-limited – try again later", icon="🚦")


if __name__ == "__main__":
    args = parse_args()
    limitless = LimitlessClient()
    transcript = load_transcript(limitless, args.date)
    model = get_model(args.model)
    main(transcript, model=model, max_retries=args.max_retries)
