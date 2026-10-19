# QuickStatements report: Hochzeitstafel Leopold I. und Claudia Felicitas (15.10.1673)

Source: Zeremonialprotokoll 2 (item not yet on Wikidata, placeholder `Q<ZA-Prot 2>`), pp./fol. 1706–1710; seating drawing on 1710.
Batch: `1673-10-15_Hochzeit_Leopold_I_Claudia_Felicitas.qs`, 19 commands. URL in `1673-10-15_Hochzeit_Leopold_I_Claudia_Felicitas.qs.url`.

The batch cannot run until `Q<ZA-Prot 2>` is replaced by the book's QID (in the .qs and in the URL).

https://www.wikidata.org/wiki/Q141775829

## Table

Seat numbering: clockwise as drawn on fol. 1710. Seat 1 is the lower position on the left side of the drawing (the Emperor's right), up that side, across the head (Kaiser, Kaiserin), down the right side. Head of table at the top, under the baldachin.

| Seat | Rank | Named as | Item | Role / office |
|---|---|---|---|---|
| 1 | 9 | "Vorschneider Frhl. von Hainrichsberg" | somevalue | seneschal (Q1138622) |
| 2 | 8 | "Vorschneider Frh. Hoyos" | somevalue | – |
| 3 | 3 | "Erzherzogin" | somevalue | – |
| 4 | 1 | "Kayser" | Leopold I (Q150494) | bridegroom |
| 5 | 2 | "Kayserin" | Claudia Felicitas (Q93541) | bride |
| 6 | 7 | "Vorschneider Graf von Mollart" | somevalue | – |
| 7 | 4 | "Nuntius Apostolicus" | Mario Alberizzi (Q3293329) | Apostolic Nuncio to Emperor (Q110602629) |
| 8 | 5 | "Spanischer Pottschaffter" | somevalue | ambassador of Spain (Q6348379) |
| 9 | 6 | "Wenedischer Pottschaffter" | somevalue | envoy of Venice (Q110620657) |
| 10 | 10 | "Vorschneider Frh. von Pranckh" | somevalue | seneschal (Q1138622) |

Opposites: 3 ↔ 6 (stated in the text), 1 ↔ 10 (text: "at the end of the table, on both sides"), 2 ↔ 8 (from the drawing only). Seats 4, 5, 7, 9 have nobody across (`novalue`).

## Derived, not stated

- All ranks are derived: sovereigns first, then the Archduchess, then nuncio, Spanish and Venetian ambassador in the order the text names them, then the four carvers by distance from the head.
- The nuncio is not named in the text. Q3293329 holds "Apostolic Nuncio to Emperor" 1671-02-28 to 1675-09-29 on Wikidata, the only holder on the date.
- Hoyos opposite the Spanish ambassador is read from the vertical position in the drawing; it could also be the nuncio.
- `P1932` values are cleaned readings of the drawing, not the raw transcription ("Erzherzogen", "Hh os", "Aplieus", "Pranikh").

## Ambiguous persons

- Seat 3 "Erzherzogin": not named. Candidates are the bride's mother Anna de' Medici, widowed Archduchess of Tyrol, and Leopold's unmarried half-sister Maria Anna Josepha. Set to somevalue; no QIDs checked.

## No Wikidata item yet

- Graf von Mollart (seat 6), Frh. von Hoyos (seat 2), Frh. von Heinrichsberg (seat 1), Frh. von Franckh/Pranckh (seat 10): no matching items found.
- Spanish and Venetian ambassadors at the imperial court in 1673: no office holders for that date on Wikidata.
- The court office "Vorschneider" (carver) has no item; Mollart and Hoyos therefore carry no `P39`.

## Open questions

- Book QID for ZA-Prot. 2: the P217 SPARQL query timed out and a label search found nothing. The book items may not exist yet.
- Are 1706–1710 folio numbers or image numbers? Used as `S7416` folio; switch to `S958 "Bild …"` if they are image numbers.
- The four carvers stood at the table and did not sit. They are included as participants with seat numbers, as in Q140068424. Drop seats 1, 2, 6, 10 if only diners should count; neighbours and ranks then need recalculation.
- Heinrichsberg and Franckh are "Truchsessen" in the text and "Vorschneider" in the drawing; `P39` uses seneschal (Q1138622).
- Location: only Graz (Q13298) is set. The transcription has "Schloss Eggenberg (?)", Ritterstube. Eggenberg Castle is Q203797 if confirmed; the Grazer Burg is the other plausible venue.
- `P31` is royal wedding (Q63442071), as on the reference item. A separate banquet item (Q626066) with `P361` to the wedding would be the alternative.
- Seven `P710 somevalue` statements: high risk that QuickStatements merges them (see the known risk in the skill reference). Check the item after the run; ten `P710` statements, one `P1545` each.
- `scripts/qs_url.py` and `data/zeremonialprotokolle.json` are missing from the skill folder. The URL was built by hand in the classic V1 encoding (tab → `|`, newline → `||`) for qs-dev.toolforge.org; check that QuickStatements 3.0 accepts it.
