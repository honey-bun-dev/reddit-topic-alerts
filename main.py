from __future__ import annotations

from pathlib import Path
from typing import Any

from reddit_client import get_reddit_client
from storage import load_json, load_seen_posts, save_json, save_seen_posts

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


def load_config(path: Path) -> dict[str, Any]:
    config = load_json(path, default={})
    if not isinstance(config, dict):
        raise ValueError("config.json must contain a JSON object.")

    subreddits = config.get("subreddits", [])
    keywords = config.get("keywords", [])

    if not isinstance(subreddits, list) or not all(isinstance(item, str) for item in subreddits):
        raise ValueError("config.json field 'subreddits' must be a list of strings.")
    if not isinstance(keywords, list) or not all(isinstance(item, str) for item in keywords):
        raise ValueError("config.json field 'keywords' must be a list of strings.")

    limit_per_subreddit = config.get("limit_per_subreddit", 20)
    if not isinstance(limit_per_subreddit, int) or limit_per_subreddit <= 0:
        raise ValueError("config.json field 'limit_per_subreddit' must be a positive integer.")

    output_file = config.get("output_file", "alerts.json")
    seen_file = config.get("seen_file", "seen_posts.json")

    if not isinstance(output_file, str) or not output_file.strip():
        raise ValueError("config.json field 'output_file' must be a non-empty string.")
    if not isinstance(seen_file, str) or not seen_file.strip():
        raise ValueError("config.json field 'seen_file' must be a non-empty string.")

    return {
        "subreddits": subreddits,
        "keywords": keywords,
        "limit_per_subreddit": limit_per_subreddit,
        "output_file": output_file,
        "seen_file": seen_file,
    }


def find_matched_keyword(title: str, keywords: list[str]) -> str | None:
    lowered_title = title.lower()
    for keyword in keywords:
        if keyword.lower() in lowered_title:
            return keyword
    return None


def run() -> None:
    config = load_config(CONFIG_PATH)
    reddit = get_reddit_client()

    output_path = BASE_DIR / config["output_file"]
    seen_path = BASE_DIR / config["seen_file"]

    existing_alerts = load_json(output_path, default=[])
    if not isinstance(existing_alerts, list):
        existing_alerts = []

    seen_posts = load_seen_posts(seen_path)
    new_alerts: list[dict[str, Any]] = []

    for subreddit_name in config["subreddits"]:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            posts = subreddit.new(limit=config["limit_per_subreddit"])

            for post in posts:
                if post.id in seen_posts:
                    continue

                matched_keyword = find_matched_keyword(post.title or "", config["keywords"])
                if matched_keyword is not None:
                    new_alerts.append(
                        {
                            "id": post.id,
                            "title": post.title,
                            "subreddit": subreddit_name,
                            "permalink": f"https://www.reddit.com{post.permalink}",
                            "url": post.url,
                            "created_utc": post.created_utc,
                            "matched_keyword": matched_keyword,
                        }
                    )

                seen_posts.add(post.id)
        except Exception as exc:
            print(f"[WARN] Failed to process r/{subreddit_name}: {exc}")

    all_alerts = existing_alerts + new_alerts
    save_json(output_path, all_alerts)
    save_seen_posts(seen_path, seen_posts)

    print(f"Scanned {len(config['subreddits'])} subreddits.")
    print(f"Found {len(new_alerts)} new matching posts.")

    if new_alerts:
        print("\nNew alerts:")
        for alert in new_alerts:
            print(
                f"- [r/{alert['subreddit']}] ({alert['matched_keyword']}) {alert['title']}\n"
                f"  {alert['permalink']}"
            )

    print(f"\nAlerts file: {output_path.name}")
    print(f"Seen IDs file: {seen_path.name}")


if __name__ == "__main__":
    run()
