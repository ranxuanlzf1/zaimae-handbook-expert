# ZaiMei · US Study & Life Handbook (WorkBuddy Expert)

[中文版](README.md) · English

Source repository for the **full-data edition** of the *Daoge the International Student* (道哥是留子) WorkBuddy expert. It bundles 25 static reference files — 607 school profiles, 532 cities, 51 states, ~1050 undergraduate majors, 303 funding routes, city and state rules — together with the Agent prompt and two Skills. The handbook itself is v3 (2026-11-28 snapshot); the package ID `zaimae-v2-handbook` is a historical codename for the same handbook.

Licensed under [CC BY-NC-SA 4.0](LICENSE). You may share and adapt it with attribution, **non-commercial use only**, and adaptations must carry the same license. Paid consulting, reselling the data, or using it as a commercial product's knowledge base requires separate written permission from the copyright holder.

**Search keywords**: study in US, international students, Chinese students in America, Daoge the International Student.

## Install from GitHub

> **One rule before anything else.** The 15 files under `references/` have Chinese filenames. **Do not extract the zip with Windows Explorer** — it decodes filenames with the local codepage, the names turn into mojibake, and every Skill lookup breaks. Use 7-Zip / Bandizip, or Python's `zipfile`.

**Option A · ready-made package (recommended)**

1. Download the latest `zaimae-v2-handbook-v1.2.0.zip` from Releases. You can also run `python tools/pack.py` and find the build in `dist/`.
2. Extract with 7-Zip / Bandizip. You get a `zaimae-v2-handbook/` folder.
3. Move the **whole folder** into your "My Experts" plugin directory:
   - Windows: `C:\Users\<you>\.workbuddy\plugins\marketplaces\my-experts\plugins\`
   - macOS / Linux: `~/.workbuddy/plugins/marketplaces/my-experts/plugins/`
4. Restart WorkBuddy. The expert appears under **Experts → My Experts**.

**Option B · build from source**

Click **Code → copy URL** on the repository page, then:

```bash
git clone <the URL you just copied>
cd zaimae-handbook-expert
python tools/pack.py
```

Then follow steps 2–4 above. The clone folder is named after the repository, which does not match `plugin.json`'s `name` (`zaimae-v2-handbook`) — never drop the repo folder straight into `plugins/`; let the pack script produce the standard folder name.

**Option C · publish to the Expert Marketplace**

Upload the zip to the [WorkBuddy Open Platform](https://open.workbuddy.cn/expert/publish?action=create&step=1) (≤ 20 MB); it parses `plugin.json` into a draft. Note that `profession.zh` must be unique within one account.

**Maintainer · first push**

```bash
git remote add origin <the URL you just copied>
git push -u origin main
```

GitHub no longer accepts account passwords over HTTPS: use a Personal Access Token or set up an SSH key. When creating the repository, do **not** initialize it with a README / license / .gitignore, or the first push will conflict.

> On Windows, `git config --global core.quotepath false` makes Chinese filenames display correctly in the terminal.

---

## What it covers

Five tracks, 147 checkpoints, school-specific answers always framed as "when to do it, and what goes wrong if you miss it":

| Track | Covered |
|---|---|
| Academics | Add/drop windows, prerequisite order, major declaration, three GPA lines, academic appeals |
| Housing | On/off campus, leases and deposits, utilities, commute and night safety |
| Social life | Three opening windows, four types of venue, online-to-offline boundaries |
| Daily life | Food, clothing, transport, essentials — supermarket tiers, cooking costs, student transit, banking and phone |
| Safety net | Insurance and waivers, SSN, tax filing, documents, consular emergencies |
| Funding (add-on) | Who can give, four kinds of money, the application timeline, five common traps |

**Data scale**: 607 school profiles in 14 volumes, 532 cities plus 15 supplements and 51 states, 607 schools in each of the housing / shopping / insurance / social tables, ~1050 majors across 13 detailed schools, 303 funding routes, 594 institutions, 12 pathways and 5 application stages.

## Answer style

**Plain language, answer first, references at the bottom.** The first sentence is the conclusion or the next thing to do. The body uses short colloquial sentences and contains no internal jargon — no "four-layer fallback", "snapshot", "live verification layer", "schoolId", "references" — and no narration of how the answer was retrieved.

All provenance goes into one **Reference index** block at the very end: handbook version, collection and review dates, school and data layer, source file, official page, and for live checks the full URL, source type, fetch time and applicable academic year. Handbook sources and live-check sources are listed on separate lines, never mixed. Two plain-language lines stay in the body: "this is the X academic-year figure, check the official page before you act" and "call 911 first in a life-threatening emergency".

## Architecture

Agent-type expert (a single AI persona) with two Skills:

| Skill | Role |
|---|---|
| `zaimae-handbook` | 15 static reference files: handbook text, school tables, major index, funding library, city/state rules; v3 structure, field dictionary, retrieval rules |
| `zaimae-live-check` | Controlled live-verification SOP: official domain allowlist, topic → official page mapping, source annotation template, conflict and failure handling |

`WebSearch` / `WebFetch` are provided by the host. The package declares no `tools` and needs no MCP server or connector — it only defines when to check, which domains, and how to cite.

**Live verification** is triggered when a school or city is not indexed, a question concerns a current deadline / fee / threshold, or the user asks for official links. The answer is assembled from general → state → city → school (the handbook itself has three layers — general → city → school — with state-level fields living in the city layer), then official `.edu`, `.gov` and consulate pages are checked. Findings are **never written back into `references/`**; anything unverifiable is marked "not verified" instead of guessed.

## Data source and licensing

- Source: online single-file site `app_17j7z4evysm`, `https://vcnl8tmrq6tg.doubao.link/app/app_17j7z4evysm`
- Snapshot: v3, 2026-11-28 (batches B01–B75, rebuilt after six-layer audit); funding library verified through 2026-11-21
- Handbook © 2026 刘忠锋 (writing as "在美"). The copyright holder has authorized this package to include the full handbook for public Q&A, including school tables, the major index, the funding library and the institution index.
- Repository license: [LICENSE](LICENSE) · CC BY-NC-SA 4.0. The "all rights reserved" line inside the handbook text serves as an attribution notice; for distribution from this repository, this license governs.
- Static snapshot only. Policies change every academic year; for signing, payment, filing, waivers and claims, the current official page prevails.
- Live-check content is **not** handbook content: it is not attributed to the handbook, never written into `references/`, and never overwrites snapshot values.

## Repository layout

```text
zaimae-handbook-expert/
├── .codebuddy-plugin/plugin.json      # Display fields and registration (declares 2 Skills)
├── agents/zaimae-v2-handbook.md       # Persona, methodology, three-layer model, compliance lines
├── avatars/expert.png                 # 512x512 ink-wash avatar
├── skills/
│   ├── zaimae-handbook/
│   │   ├── SKILL.md
│   │   └── references/                # 15 files: handbook text + 01-11 topic datasets
│   └── zaimae-live-check/SKILL.md
├── README.md / README.en.md
├── LICENSE
├── .gitignore / .gitattributes
└── tools/pack.py
```

`LICENSE`, `README.en.md`, `.gitignore`, `.gitattributes` and `tools/` are repository-only files; `tools/pack.py` excludes them from the importable zip.

## Example prompts

- "List the milestones I need to watch this semester for my school: add/drop, GPA thresholds, insurance waiver"
- "It's week three and I feel I've missed something. Walk me through a check in order."
- "For my school: where do students gather near campus, how do I draw my social radius in the city, and is the commute worth it?"
- "Which undergraduate majors does UCSB's College of Letters and Science offer, and what degree does each grant?"
- "Which funding routes in the library fit international master's students?"

## Boundaries

Milestones, rules and risk flags only. No application handling, no ghostwriting, no form filling, no sending mail on the user's behalf; not legal, tax, visa, medical or mental-health advice. Call 911 first in a life-threatening emergency. Live checks verify rules and locate official pages — they do not turn the expert into an agent that acts for the user or into a real-time data service.

## Maintain

`tools/pack.py` builds a zip whose top-level folder is `zaimae-v2-handbook/` (matching `plugin.json`'s `name`) and sets UTF-8 flags on non-ASCII filenames. It excludes `.git/`, `LICENSE`, `tools/` and any zip. Output: `dist/zaimae-v2-handbook-v<version>.zip`.

After changing `plugin.json`, `agents/*.md` or any `SKILL.md`, re-validate and re-register; data-only changes under `references/` need a new zip but no re-registration:

```bash
python <WorkBuddy>/skills/expert-manager/scripts/validate_expert.py <expert-dir>
python <WorkBuddy>/skills/expert-manager/scripts/register_expert.py <expert-dir>
```

To update the handbook data: edit the handbook site → re-export → regenerate `references/` → verify the key counts (1050 majors, 303 funding routes, 607 school tables, 594 institutions) → rebuild the zip. Schools discovered through live checks must go through the handbook-side update before they can be added to `references/`.
