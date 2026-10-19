---
name: imperial-table-graph
description: >-
  Turn a seating arrangement recorded in a historical source — above all the
  Viennese court's Zeremonialprotokolle (AT-OeStA/HHStA OMeA ZA-Prot.,
  1652–1918) — into a Wikidata event item whose participants (P710) carry
  seat number, precedence rank, neighbours and the person seated opposite.
  Use whenever the user gives a transcription, excerpt or description of a
  court banquet, wedding table, Hoftafel, offene Tafel, Tafelordnung,
  Sitzordnung or seating plan and wants it on Wikidata, or says "extract the
  seating", "make a QuickStatements batch for this table", "create the
  wedding item like Q140068424". Identifies courtiers via the Kaiser und
  Höfe database (kaiserhof.geschichte.lmu.de, P1818) and creates person items
  for well-documented participants who have none. Outputs QuickStatements 3.0
  batches (V1 commands) plus their batch URLs.
---

# Seating arrangement → Wikidata event item

Input: a source text (transcription, excerpt, or a description of a seating
drawing) for one event, plus its archival location (volume, folio). Reference
item: [Q140068424](https://www.wikidata.org/wiki/Q140068424), the 1685 wedding
of Max II Emanuel and Maria Antonia.

`<base>` = `YYYY-MM-DD_<short event name>` with underscores
(`1685-07-15_Hochzeit_Max_Emanuel_Maria_Antonia`). Output, all in `batches/`:

| File | Written in | Spec |
|---|---|---|
| `<base>.qs` | Step 4 | `references/quickstatements.md` |
| `<base>.qs.url` | Step 4 | `scripts/qs_url.py` |
| `<base>.qs-report.md` | Step 4 | `references/quickstatements.md` |
| `<base>_persons.qs` (+ `.url`) | Step 4, only if new persons or KH IDs | `references/persons.md` |

## Working rules

- Run Steps 1–5 in one go. Stop only at the ⛔ points.
- Read each reference file once, when its step starts.
- Send independent lookups in parallel.
- Never invent persons, offices, dates, QIDs or PIDs. Anything the text does
  not say stays out of the batch and goes into the report.

## Step 1 — Read the source

> TODO: refine once the first text sample from the Zeremonialprotokolle is
> available (typical wording, abbreviations, how seats are enumerated, how
> drawings are described).

From the text, note:

1. **Event**: kind (wedding, banquet, public dining, baptism …), date, place
   (palace, room), host.
2. **Source location**: the book (`ZA-Prot. 4`), folio (`140r`) or image
   number, and the Commons file of the page if there is one. Look the book up
   in `data/zeremonialprotokolle.json` (years covered, archive URL, image
   number where each year starts) and take its QID from the book table in
   `references/quickstatements.md` (books 1–17, 1652–1740).
3. **Table geometry**: table shape, which side is the head, and the direction
   in which the source counts or draws the seats.

⛔ The text describes several tables or events → ask which one to do, or do
one batch per table/event.

⛔ The event falls outside 1652–1740 (books 1–17) → ask before going on.

## Step 2 — Seating ledger

One line per seat, in the order the source gives them:

```
SEAT 6 | "Ihre Kays. May." | rank 1 | Leopold I | role – | office – | opp none
SEAT 4 | "die Durchl. Braut" | rank 4 | Maria Antonia | role bride | office – | opp 8
SEAT 1 | "ein Truchsess"   | rank 10 | (unnamed) | role – | office seneschal | opp 11
PROBLEM unclear | seat 9: "Cammerherr" – which one?
```

- **Seat numbers** (`P1545`) run 1…n along the table in one direction; keep
  that direction for the whole event and state it in the report. Neighbours
  (`P155`/`P156`) follow from it: seat n−1 and n+1.
- **Rank** (`P1352`) is the order of precedence, 1 = highest. Take it from
  the text if stated; otherwise derive it from the seating logic of the source
  and mark it as derived in the report.
- **Opposite** (`P461`): only for seats with a seat across the table.
- Keep the name exactly as written: it becomes `P1932` (object named as).

## Step 3 — Reconcile persons and offices

Read `references/persons.md`.

1. For each named person: `search_items` (native name, regnal name, title),
   then `get_statements` to confirm (birth/death dates fit the event date,
   family, office).
2. For every courtier, also look them up in **Kaiser und Höfe**
   (`https://kaiserhof.geschichte.lmu.de/<id>`, Wikidata `P1818`). It covers
   the Habsburg court staff of the 16th–17th centuries with offices, dates,
   family and GND links, and is often the only way to tell which Harrach or
   Hoyos sat at the table. Do this even when a Wikidata item turns up: the KH
   offices confirm the match.
3. Offices and roles (`P39`, `P3831`): reuse the QIDs in
   `references/quickstatements.md`, otherwise `search_items` +
   `get_statements`.
4. ⛔ A person matches several items or KH records equally well → don't pick
   one; use `somevalue` with the office and list the candidates in the report.
5. A person identified in KH (or GND, or another citable reference) with full
   name and a birth or death year, but with no Wikidata item → create one in
   `<base>_persons.qs` (rules in `references/persons.md`). An existing item
   without `P1818` gets its KH ID in the same batch.
6. A person with no item and not enough for a new one (only family name and
   office, no KH/GND record) → `somevalue` + `P39`/`P1932`; list under "No
   Wikidata item yet".

## Step 4 — QuickStatements batch

Read `references/quickstatements.md`, then:

1. Check that no event item exists yet (`search_items` for the event, and a
   SPARQL query for items with `P710` of the main persons and the same
   `P585`). Exists → write an update batch against that QID instead of
   `CREATE`.
2. Write `<base>.qs` and `<base>.qs-report.md`. Prefix every
   `P710 somevalue` line with `+`, or QuickStatements merges the unnamed
   seats into one statement.
3. New persons → also write `<base>_persons.qs`, and in `<base>.qs` use the
   placeholder `Q<new: Name>` for them (see `references/persons.md`).
4. Run `python3 scripts/qs_url.py` on `batches/<base>_persons.qs` (if any)
   and `batches/<base>.qs`. With placeholders, the event batch is refused
   until the persons batch has run and the QIDs are filled in; say so in the
   hand-over.

## Step 5 — Hand over

In the final message: name the files, give the batch URL(s) in run order
(persons first), and list the open questions from the report. Then stop.
