from __future__ import annotations

import os

import praw
from dotenv import load_dotenv

REQUIRED_ENV_VARS = [
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "REDDIT_USER_AGENT",
]


def get_reddit_client() -> praw.Reddit:
    load_dotenv()

    missing_vars = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing_vars:
        missing_text = ", ".join(missing_vars)
        raise RuntimeError(
            f"Missing required environment variables: {missing_text}. "
            "Create or update your .env file before running the script."
        )

    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )
    reddit.read_only = True
    return reddit
