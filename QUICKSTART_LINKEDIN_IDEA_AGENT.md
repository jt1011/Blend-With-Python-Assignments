# Quickstart: LinkedIn Idea Agent MVP

## 0) Capture posts from X with extension (new)
1. Load unpacked extension from `extension/twitter_feed_capture_extension` in Chrome Developer Mode.
2. Open `x.com/home` while logged in.
3. Start run in popup and let it collect posts.
4. Export `captured_posts.json`.

## 1) Run with sample data
```bash
python3 linkedin_idea_agent.py --input sample_captured_posts.json --target 10
```

Outputs:
- `linkedin_ideas_report.md`
- `linkedin_ideas_report.json`

## 2) Run with your captured feed data
```bash
python3 linkedin_idea_agent.py --input /path/to/captured_posts.json --target 100
```

## 3) Minimum input schema
Each post should include:
- `text`
- `url`

Recommended fields for better ranking:
- `likes`
- `reposts`
- `replies`
- `author`
- `tweet_id`

## 4) Next upgrade
Switch idea generation from heuristic to local LLM (`ollama`) once this baseline is validated.
