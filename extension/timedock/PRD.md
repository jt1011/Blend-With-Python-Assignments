# TimeDock — Lean Product Requirements Document (PRD)

## One-line summary
**TimeDock** is a lightweight Chrome side-panel extension that helps professionals quickly view cross-timezone clocks, convert meeting times, and avoid scheduling mistakes without leaving the current tab.

## Problem
People working with distributed clients repeatedly convert times manually (e.g., “9 PM PST”), causing context switching, errors, and avoidable scheduling friction.

## Goal
Ship a fast, low-memory utility that:
- lives in Chrome Side Panel
- is always quickly accessible
- converts time reliably across saved zones
- stays local-first and permission-minimal

## Primary user
Solo operators, freelancers, consultants, agency owners, recruiters, PMs, and coaches coordinating meetings across multiple regions.

## MVP scope

### 1) Persistent side panel (MV3)
- Side panel opens from extension action icon.
- Panel remains available across tabs.

### 2) Saved timezone cards
Default zones:
- Local timezone
- `America/Los_Angeles` (PT)
- `America/New_York` (ET)
- `UTC`

Per card:
- current time
- day rollover label (`Yesterday` / `Today` / `Tomorrow`)
- timezone label
- work-hours indicator (`Within work hours` / `Outside work hours`)

### 3) Quick converter
- User enters time (e.g., `9:00 PM`).
- User selects source timezone.
- Converted output appears for all saved zones.

### 4) Overlap strip
Show compact overlap between two zone schedules (home vs selected client zone):
- home hours
- client hours
- best overlap window

### 5) Abbreviation helper
Support common aliases (`PST`, `EST`, etc.) as input helpers, but always map internally to IANA timezone IDs.

### 6) Copy-ready outputs
One-click templates:
- `9:00 PM PT = 10:30 AM IST`
- `Thu, 9 PM PT / Fri, 10:30 AM IST`

### 7) Lightweight settings
- saved timezone list (add/remove/reorder)
- 12h/24h format
- work hours per zone
- home timezone
- compact mode toggle

## Explicitly out of scope for v1
- Calendar integrations
- AI parsing
- Slack/Gmail integrations
- Team collaboration
- Meeting booking links
- Tab/page injection features
- Analytics dashboards
- Cloud sync

## Functional requirements
- Side panel loads quickly (target under 300ms after initial extension load).
- Time display updates once per minute.
- Converter handles date rollover and 12 AM/PM cases.
- Settings persist through browser restarts via local storage.

## Non-functional requirements
- No external API dependency for core timezone logic.
- Event-driven architecture; minimal idle background work.
- Minimal permissions: `sidePanel`, `storage`.
- No host permissions in MVP.

## Technical approach (v1)
- Manifest V3 extension
- `sidepanel.html`, `sidepanel.js`, `styles.css`
- small background service worker for side panel behavior
- `chrome.storage.local` for persistence
- `Intl.DateTimeFormat` and related `Intl` APIs for timezone formatting

## Lean data model
```json
{
  "homeTimezone": "Asia/Kolkata",
  "savedTimezones": [
    "Asia/Kolkata",
    "America/Los_Angeles",
    "America/New_York",
    "UTC"
  ],
  "timeFormat": "12h",
  "workingHours": {
    "Asia/Kolkata": { "start": "10:00", "end": "19:00" },
    "America/Los_Angeles": { "start": "09:00", "end": "18:00" },
    "America/New_York": { "start": "09:00", "end": "18:00" }
  },
  "compactMode": true,
  "lastSourceTimezone": "America/Los_Angeles"
}
```

## Edge cases
- DST transitions
- ambiguous abbreviations (`CST`)
- cross-day conversion shifts
- invalid time input
- `12 AM` vs `12 PM`

## Acceptance criteria (MVP)
1. Opens in Chrome Side Panel from toolbar action.
2. Shows current time for selected zones immediately.
3. Converts one entered time from source zone to all saved zones.
4. Persists settings via local storage.
5. Keeps idle footprint low with no unnecessary background loops.
6. Requires no external APIs for timezone conversion.

## Delivery phases
- **Phase 1 (this PR):** PRD finalized and approved.
- **Phase 2:** Extension scaffold + side panel UI + storage + converter logic.
- **Phase 3:** DST/overlap hardening, compact UI polish, packaging for local install.
