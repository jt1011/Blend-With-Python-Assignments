# Quickstart: LinkedIn Idea Agent MVP

## 1) Run with sample data
```bash
python3 linkedin_idea_agent.py --input sample_captured_posts.json --target 10
```

Outputs:
- `linkedin_ideas_report.md`
- `linkedin_ideas_report.json`

## 2) Run with your own captured feed data
```bash
python3 linkedin_idea_agent.py --input /path/to/your/captured_posts.json --target 100
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
