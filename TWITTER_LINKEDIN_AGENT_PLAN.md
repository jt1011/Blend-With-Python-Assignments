# Twitter Feed-Scroller Extension → LinkedIn Idea Agent Plan

## Short answer to your question
**Yes — it is possible** to build this as a **browser extension that scrolls your X/Twitter feed**, captures relevant posts, and generates a report (without depending on the X API).

But you should expect tradeoffs:
- More brittle than API-based ingestion (UI changes can break selectors).
- Must be careful with platform rules and account safety.
- Requires your browser session/login to be active.

---

## Goal
Build an extension-driven assistant that runs for 1–2 hours, auto-scrolls your feed, captures software-engineering content, and returns ~100 non-duplicate “root ideas” for LinkedIn posts.

---

## Product definition (what “done” looks like)
After a run, you get:
1. **100 root ideas**.
2. For each idea:
   - one-line takeaway,
   - why it matters to engineers,
   - source tweet URLs,
   - optional LinkedIn hook angle.
3. A grouped digest report (Markdown / Notion / Google Doc).
4. Quality + duplicate confidence score.

---

## Extension-first architecture (no API dependency)
1. **Chrome Extension (Manifest V3)**
   - Popup UI: start/stop run, duration, topic profile.
   - Background service worker: orchestrates run state.
   - Content script on `x.com`: scroll + extract tweet cards.

2. **Capture pipeline (inside extension)**
   - Read visible tweet DOM nodes.
   - Extract: text, author, timestamp, url, engagement metrics when present.
   - De-duplicate by tweet ID.
   - Buffer locally (IndexedDB) and batch-send to backend.

3. **Backend processing service**
   - Receives captured posts.
   - Filters for software engineering relevance.
   - Extracts candidate ideas with LLM.
   - Clusters + ranks + de-duplicates ideas.

4. **Report generator**
   - Produces top 100 ideas.
   - Adds citations/links and category buckets.
   - Delivers to email/Notion/Markdown export.

---

## “Agenty” run behavior (2-hour autonomous session)
1. You open X home feed and click **Start Run (120 min)**.
2. Extension performs human-like scrolling intervals.
3. It pauses randomly, opens promising threads, then returns.
4. It collects and sends posts in small batches every few minutes.
5. Backend continuously scores and clusters ideas.
6. At end, system finalizes top 100 and delivers report.

---

## Safety + reliability guardrails (important)
- Use conservative scrolling speed and randomized delays.
- Include max actions/minute limits.
- Provide emergency stop button.
- Keep extraction read-only (no likes/replies/follows).
- Log selector failures and auto-fallback selectors.
- Save checkpoints every few minutes in case tab crashes.

---

## Data model (minimum)
- `runs` (start/end/status/config)
- `captured_posts` (tweet_id, text, author, url, seen_at, raw_meta)
- `idea_candidates` (post_id, idea_text, confidence, tags)
- `idea_clusters` (cluster_id, representative_idea, members)
- `ranked_ideas` (run_id, score, rationale, citations)

---

## Ranking rubric for root ideas
Score each idea (1–5):
- Software engineering relevance
- Practicality/usefulness
- Novelty/freshness
- Specificity
- Evidence strength (quality of supporting posts)

Ship ideas above threshold first, then fill to 100 by rank.

---

## What can break (and how to mitigate)
1. **DOM/UI changes on X**
   - Maintain selector map + quick patch workflow.
2. **Session/logged-out issues**
   - Pre-run checks for authenticated state.
3. **Low signal from home feed**
   - Add optional mode: auto-open curated lists/bookmarks/search pages.
4. **Duplicate content loops**
   - Track seen tweet IDs and text hashes.

---

## MVP roadmap (extension-first)

### Phase 1 (Week 1): Feed capture prototype
- Build extension that scrolls + extracts tweet cards.
- Save captured tweets locally + export JSON.
- Validate 60-minute stability.

### Phase 2 (Week 2): Processing + report
- Add backend ingestion endpoint.
- Add filtering, idea extraction, and dedup.
- Deliver top 30–50 ideas report.

### Phase 3 (Week 3): 2-hour production run
- Improve reliability, retries, checkpoints.
- Add ranking and theme grouping.
- Hit ~100 ideas on strong-signal days.

### Phase 4 (Week 4): Personalization + publishing workflow
- Learn your accepts/rejects.
- Add LinkedIn hook generator in your voice.
- Add one-click export to your writing workspace.

---

## Success metrics
- **Coverage**: 80–100 ideas per 2-hour run initially; target stable 100.
- **Usability**: ≥70% ideas marked usable by you.
- **Dedup quality**: <10% near duplicates.
- **Runtime stability**: ≥90% runs complete without manual intervention.

---

## Practical first build checklist
1. Build extension scaffold (popup + background + content script).
2. Implement safe auto-scroll loop with stop/resume.
3. Parse tweet cards and persist to IndexedDB.
4. Add backend endpoint to receive batches.
5. Add LLM extraction + embedding dedup.
6. Generate first 60-minute report and evaluate quality.

---

## Recommended stack
- **Extension**: TypeScript + Manifest V3.
- **Backend**: Python (FastAPI).
- **DB**: Postgres (+ pgvector for semantic dedup).
- **LLM**: GPT-class model for extraction + summarization.
- **Jobs**: Celery/RQ for report generation.

---

## Suggested output format (for each idea)
- **Idea**: one-sentence root claim.
- **Why now**: context in 1 sentence.
- **LinkedIn angle**: practical/contrarian hook.
- **Evidence**: 2–3 tweet links.
- **Confidence**: High / Medium / Low.

---

## Immediate next step
Start with a **60-minute extension pilot** on your home feed + one curated list. If that yields at least 40 usable ideas, scale to full 2-hour runs and optimize for consistent 100-idea delivery.
