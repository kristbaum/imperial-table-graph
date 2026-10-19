# imperial-table-graph

A Claude skill that turns seating arrangements from the Viennese court's
Zeremonialprotokolle (AT-OeSTA/HHStA OMeA ZA-Prot., 1652–1918) into Wikidata
event items, modelled on [Q140068424](https://www.wikidata.org/wiki/Q140068424).

- `SKILL.md`: workflow
- `references/quickstatements.md`: data model and QuickStatements V1 format
- `scripts/qs_url.py`: writes the QuickStatements 3.0 batch URL for a `.qs` file
- `batches/`: generated batches (`<base>.qs`, `<base>.qs.url`, `<base>.qs-report.md`)

```
python3 scripts/qs_url.py batches/<base>.qs
```
