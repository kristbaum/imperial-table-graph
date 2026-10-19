# imperial-table-graph

A Claude skill that turns seating arrangements from the Viennese court's
Zeremonialprotokolle (AT-OeSTA/HHStA OMeA ZA-Prot., 1652–1918) into Wikidata
event items, modelled on [Q140068424](https://www.wikidata.org/wiki/Q140068424).

- `SKILL.md`: workflow
- `references/quickstatements.md`: data model and QuickStatements V1 format
- `references/persons.md`: identifying participants (Kaiser und Höfe, P1818) and creating person items
- `scripts/qs_url.py`: writes the QuickStatements 3.0 batch URL(s) for a `.qs` file
- `scripts/scrape_series.py`: scrapes a series' units from archivinformationssystem.at
- `scripts/build_series_qs.py`: builds the book-item and book-link batches from that scrape
- `data/zeremonialprotokolle.json`: all units of the Zeremonialprotokolle series
- `batches/`: generated batches (`<base>.qs`, `<base>.qs.url`, `<base>.qs-report.md`)

```
python3 scripts/qs_url.py batches/<base>.qs
```

## Building the `.skill` file

A `.skill` file is a plain zip archive with `SKILL.md` and `references/` at the
archive root. Rebuild it after editing either one:

```sh
rm -f imperial-table-graph.skill
zip -r imperial-table-graph.skill SKILL.md references
```