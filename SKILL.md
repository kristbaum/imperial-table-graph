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
  wedding item like Q140068424". Outputs a QuickStatements 3.0 batch (V1
  commands) plus its batch URL.
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
   number where each year starts).
3. **Table geometry**: table shape, which side is the head, and the direction
   in which the source counts or draws the seats.

⛔ The text describes several tables or events → ask which one to do, or do
one batch per table/event.

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

1. For each named person: `search_items` (native name, regnal name, title),
   then `get_statements` to confirm (birth/death dates fit the event date,
   family, office). `P1818` Kaiser und Höfe ID helps for courtiers.
2. Offices and roles (`P39`, `P3831`): reuse the QIDs in
   `references/quickstatements.md`, otherwise `search_items` +
   `get_statements`.
3. ⛔ A person matches several items equally well → don't pick one; use
   `somevalue` with the office and list the candidates in the report.
4. A person with no item → `somevalue` + `P39`/`P1932`; list under "No
   Wikidata item yet".

## Step 4 — QuickStatements batch

Read `references/quickstatements.md`, then:

1. Check that no event item exists yet (`search_items` for the event, and a
   SPARQL query for items with `P710` of the main persons and the same
   `P585`). Exists → write an update batch against that QID instead of
   `CREATE`.
2. Write `<base>.qs` and `<base>.qs-report.md`.
3. Run `python3 scripts/qs_url.py batches/<base>.qs` to write
   `<base>.qs.url`.

## Step 5 — Hand over

In the final message: name the files, give the batch URL, and list the open
questions from the report. Then stop.
