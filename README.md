# reddit-topic-alerts

Private, local, read-only Reddit keyword monitoring script for personal use.

This project uses the Reddit API via PRAW to read recent public posts from selected subreddits and find title matches for your configured keywords.

## Important behavior

- Python 3.11+
- Read-only usage only
- No posting, commenting, voting, messaging, or any write actions
- Stores only small metadata locally in JSON files

## Project files

- `main.py`: Runs monitoring, keyword matching, output, and dedupe flow
- `reddit_client.py`: Creates a Reddit client from `.env` values
- `storage.py`: JSON load/save helpers and seen-post ID helpers
- `config.json`: Subreddits, keywords, and file settings
- `.env.example`: Environment variable template
- `requirements.txt`: Python dependencies

## Reddit app setup

1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **create app**
3. Set **App type** to `script`
4. Set **Redirect URI** to `http://localhost:8080`
5. Copy the generated client ID and client secret

## Installation

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Fill in your Reddit credentials in `.env`:

```env
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
REDDIT_USER_AGENT=windows:reddit-topic-alerts:v1.0 by /u/YOUR_USERNAME
```

3. Update `config.json` with your target subreddits and keywords

Example `config.json`:

```json
{
  "subreddits": ["Python", "webdev", "nextjs", "Supabase", "artificial", "Bittensor", "programming"],
  "keywords": ["python", "next.js", "supabase", "ai agent", "bittensor", "api"],
  "limit_per_subreddit": 20,
  "output_file": "alerts.json",
  "seen_file": "seen_posts.json"
}
```

## Run

```powershell
python main.py
```

## Output

- Matches are appended to `alerts.json`
- Processed post IDs are stored in `seen_posts.json` to avoid duplicate alerts
- Each alert stores:
  - `id`
  - `title`
  - `subreddit`
  - `permalink`
  - `url`
  - `created_utc`
  - `matched_keyword`

## Notes

- The script processes each subreddit independently and continues if one subreddit fails.
- Keep `limit_per_subreddit` moderate to stay simple and respectful of API usage.
