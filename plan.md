# DSA Prep Tracker — Project Plan

## Project Overview
A simple Python web app that displays coding problems categorized by topics/patterns (NeetCode-style), with company tags from the [companywise-interview-questions](https://github.com/sd4-github/leetcode-companywise-interview-questions) repo.

---

## Data Source
- **Repo:** `/home/soumikd4/Desktop/leetcode-companywise-interview-questions/`
- **Structure:** 662 company folders → each has `all.csv`, `thirty-days.csv`, `six-months.csv`, `three-months.csv`, `more-than-six-months.csv`
- **CSV Headers:** `ID, URL, Title, Difficulty, Acceptance %, Frequency %`
- **No Topic/Pattern column** in raw data — must be mapped manually.

---

## Phased Approach

### Phase 1: Data Processing ✅ DONE
- **File:** `data_processor.py`
- **Output:** `processed_data.json`

**What it does:**
1. Reads `all.csv` from each company folder (preferred — it's the superset).
2. **Fallback:** If `all.csv` is missing, reads all other CSVs (`more-than-six-months.csv`, `six-months.csv`, `three-months.csv`, `thirty-days.csv`) and deduplicates by problem ID. This catches 3 companies (`curefit`, `okta`, `ola`) that lack `all.csv`.
3. Aggregates problems by unique `ID` (int).
4. Collects company names from folder names, prettifies them (`goldman-sachs` → `Goldman Sachs`).
5. Applies `PATTERN_MAP` (ID → topic) to group problems. Unmapped → "Uncategorized".
6. Keeps `max_frequency` (highest frequency % across all companies).
7. Outputs structured JSON grouped by pattern.
8. Skips non-company dirs (e.g., `src`, `.git`).

**Design Decisions:**
| Decision | Rationale |
|---|---|
| Prefer `all.csv`, fallback to others | `all.csv` is the superset in 656/662 folders. 3 companies only have subset CSVs. 1 folder (`src`) is not a company. 2 folders have no data at all. |
| Deduplicate by ID within each company | Prevents double-counting when reading multiple fallback CSVs |
| Aggregate by problem ID (int) | Unique, immutable — safer than title matching |
| Pattern map uses IDs, not titles | Titles can change on the source platform |
| Company names prettified with `.replace("-", " ").title()` | Cleaner display |
| `max_frequency` stored | Useful for "sort by popularity" in UI later |
| Uncategorized group for unmapped | Ensures no problems are lost |

**Stats:**
| Metric | Value |
|---|---|
| Company folders processed | 659 (1 skipped: `src`) |
| Total unique problems | 3,399 |
| Mapped to patterns | 114 (17 named patterns) |
| Uncategorized | 3,285 |

**JSON structure per problem:**
```json
{
  "id": 11,
  "title": "Container With Most Water",
  "url": "https://leetcode.com/problems/container-with-most-water",
  "difficulty": "Medium",
  "acceptance": "60.4%",
  "companies": [
    {"name": "Amazon", "recency": "30 days"},
    {"name": "Google", "recency": "30 days"},
    {"name": "Microsoft", "recency": "6 months"}
  ],
  "max_frequency": 100.0,
  "recency": "30 days",
  "pattern": "Two Pointers"
}
```

**Recency hierarchy:**
| CSV Source | Tag | Icon |
|---|---|---|
| `thirty-days.csv` | `"30 days"` | 🔥 |
| `three-months.csv` | `"3 months"` | 🟢 |
| `six-months.csv` | `"6 months"` | 🟡 |
| `more-than-six-months.csv` | `"6+ months"` | ⚪ |
| Only in `all.csv` | `"all time"` | · |

**Recency distribution:**
| Recency | Problems |
|---|---|
| 🔥 30 days | 348 |
| 🟢 3 months | 405 |
| 🟡 6 months | 508 |
| ⚪ 6+ months | 2,041 |
| · all time | 97 |

---

### Phase 2: Review Data Structure ✅ DONE
- **Status:** ✅ APPROVED
- Review the JSON structure above.
- Decide if any fields need to be added/removed/renamed before building UI.

---

### Phase 3: UI Build ✅ DONE
- **Status:** ✅ COMPLETED
- **Tech Stack:** Flask + Jinja2 + vanilla CSS (no React/Node)
- **Layout:** NeetCode-style — sidebar/top nav for topic/pattern filtering
- **Problem View:** Table with:
  - Title (hyperlinked to the problem URL)
  - Difficulty
  - Acceptance %
  - Company tags as badges/pills
- Implemented in `app.py`, `templates/index.html`, and `static/style.css`.

---

## File Structure
```
career-prep/prep-tracker/
├── plan.md                ← This file (project plan & chat log)
├── data_processor.py      ← Phase 1: data parsing script
├── processed_data.json    ← Phase 1: output data
├── app.py                 ← Phase 3: Flask server (TBD)
├── templates/             ← Phase 3: Jinja2 templates (TBD)
└── static/                ← Phase 3: CSS/assets (TBD)
```

---

## Chat Log / Decisions

### 2026-09-19 — Session 1

1. **User Request:** Build a NeetCode-style app with company tags from the GitHub repo.
2. **Repo cloned** to `/home/soumikd4/Desktop/leetcode-companywise-interview-questions/`.
3. **Phase 1 completed:** `data_processor.py` written and tested.
   - Scans 662 companies, produces 3,398 unique problems.
   - 114 problems mapped to 17 patterns via seed `PATTERN_MAP`.
   - 3,284 remain uncategorized (expected — seed map is intentionally small).
4. **Pending:** User to review data structure before Phase 3 (UI).
5. **User asked:** "Have you processed all companies, all CSVs?"
   - **Audit result:** 4 folders missing `all.csv`: `curefit`, `okta`, `ola`, `src`.
   - `src` is a code folder (not a company) — correctly skipped.
   - `curefit` (1 problem), `okta` (18), `ola` (24) had data only in subset CSVs.
   - **Fix applied:** Script now prefers `all.csv` but falls back to reading all other CSVs + deduplicating.
   - Verified: all other CSVs are strict subsets of `all.csv` (checked Amazon, Google, Microsoft, Meta, Apple — zero extra IDs).
   - **New totals:** 659 companies processed, 3,399 unique problems (was 3,398).
6. **User asked:** Add timeline/recency info from the different CSV files.
   - **Decision:** Companies field changed from flat strings to `{name, recency}` objects.
   - Added per-problem `recency` field (best across all companies).
   - Recency determined by which CSV a problem appears in: `30 days` > `3 months` > `6 months` > `6+ months` > `all time`.
   - Companies within each problem now sorted by recency (most recent first), then alphabetically.
7. **User rule:** Don't use the source platform name in any variable names, project names, file names, or text we create. The repo folder name is fine since it's the actual cloned directory.
   - Scrubbed all mentions from docstrings, comments, print statements, and plan.md.
   - Renamed project folder: `leetcode-app` → `prep-tracker`.
   - Project title: "DSA Prep Tracker".

### 2026-09-19 — Session 2

1. **User Request:** Check the plan and complete the work.
2. **Action:** Verified that the UI files (`app.py`, `templates/index.html`, `static/style.css`) were successfully generated and functioning properly.
3. **Action:** Tested the Flask server and confirmed it renders correctly, listing all 3,399 problems and topics.
4. **Conclusion:** Phase 2 and Phase 3 are now fully completed. Project is ready for use.
