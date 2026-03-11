# Execution Plan (ASAP) — Low-RAM LinkedIn Idea Agent

## What we are building now
A **two-part system** so your browser does not stay heavy all day:
1. **Light capture mode**: small collector session (short runs) captures feed posts.
2. **Offline intelligence mode**: local/open-source model pipeline processes captured posts and generates the final report.

This reduces extension runtime and RAM pressure.

---

## Phase A (Immediate: today)
- Use `linkedin_idea_agent.py` to process captured feed JSON.
- Rank with intelligence = relevance + engagement metrics + dedup.
- Output:
  - `linkedin_ideas_report.md`
  - `linkedin_ideas_report.json`

### Input format expected
A JSON array with fields like:
- `tweet_id` / `id`
- `text`
- `author`
- `url`
- `likes`, `reposts`, `replies`

---

## Phase B (Next: 1–2 days)
Build tiny collector options (pick one):
1. **Extension capture burst mode**
   - Run only 10–15 minute bursts, not full 2 hours.
   - Save JSON batches.
2. **Desktop browser automation runner**
   - Scheduled headless/controlled browser session captures data.
   - No always-loaded extension.

---

## Phase C (Intelligence upgrade: local model)
Replace heuristic idea generation with local open-source model:
- Option 1: `Ollama` + `llama3.1:8b-instruct` (good quality, moderate RAM).
- Option 2: `phi3:mini` / `qwen2.5:3b` (lower RAM, faster).

Use local embeddings for better dedup/clustering:
- `sentence-transformers/all-MiniLM-L6-v2`.

---

## Phase D (Reliability + productization)
- Add checkpoints and retry queue.
- Add account/topic personalization.
- Add Notion/Google Docs export.
- Add quality feedback loop (`accept` / `reject`) to retrain ranking.

---

## Quality intelligence formula (current MVP)
`score = 0.65 * relevance + 0.25 * engagement + 0.10 * content_length_bonus`

Where:
- relevance = software engineering keyword match score
- engagement = log-scaled likes/reposts/replies
- dedup = cluster-level best-post selection

---

## Why this matches your request
- Works without relying on X API.
- Supports your idea of adding intelligence via ranking and engagement signals.
- Supports low-RAM strategy by moving heavy work to offline processing and optional small local models.

---

## Next action
Run a first dataset through the script and validate if idea quality is usable for your LinkedIn workflow. Then we add local-model generation in the next iteration.
