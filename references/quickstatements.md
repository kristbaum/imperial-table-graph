# QuickStatements batch (V1 commands)

Target: QuickStatements 3.0 (`qs-dev.toolforge.org`), V1 commands. You write
`<base>.qs` and `<base>.qs-report.md`; `scripts/qs_url.py` writes the batch URL.

## Inputs

1. The seating ledger (Step 2) and the reconciled QIDs (Step 3).
2. The source location: book (volume) of the Zeremonialprotokolle, folio or
   image number, Commons file. `data/zeremonialprotokolle.json` lists every
   book with its signature, years, archive URL and, in `comments`, the image
   number where each year's entries begin.

## Fixed IDs

| What | ID | Note |
|---|---|---|
| Zeremonialprotokolle (series) | `Q<ZA-Prot>` | not created yet — batch `batches/Zeremonialprotokolle.qs`; replace the placeholder once it has a QID |
| Zeremonialprotokoll book *n* | `Q<ZA-Prot n>` | one item per book, `P179` series + `P1545` *n*; batches `batches/Zeremonialprotokolle_books.qs` and `_links.qs`. Find the QID with SPARQL on `P217` = `AT-OeStA/HHStA OMeA ZA-Prot. n` |
| Österreichisches Staatsarchiv | `Q306721` | HHStA has no item of its own |
| Hofburg, Vienna | `Q46242` | |
| royal wedding | `Q63442071` | |
| banquet | `Q626066` | |
| state banquet | `Q7603676` | |
| bridegroom / bride | `Q854830` / `Q353673` | `P3831` roles |
| chamberlain (Kammerherr) | `Q264323` | `P39` |
| seneschal (Truchsess) | `Q1138622` | `P39` |
| senior chamberlain (Obersthofmeister) | `Q2790613` | `P39` |
| ambassador of Spain | `Q6348379` | `P39` |
| envoy of the Republic of Venice | `Q110620657` | `P39` |

Add new IDs here when you confirm them.

## Event item

| Fact | Command | Ref |
|---|---|---|
| Label | `Lde`, `Len`: "Hochzeit von X und Y" / "wedding of X and Y" | no |
| Description | `Dde`, `Den`: "Hochzeit 1685 in Wien" / "1685 wedding in Vienna" | no |
| Instance of | `P31` event type (table above) | no |
| Location | `P276` palace or room | yes |
| Date | `P585` time, `/11` if the day is known | yes |
| Image | `P18` Commons file of the protocol page, quoted, without `File:` | no |
| Described by source | `P1343 Q<ZA-Prot n>` (the book) + `P7416` folio | no |
| Participants | `P710`, one statement per seat (below) | yes |

## Participants (P710)

One statement per seat, **all qualifiers and the reference on one line**.

| Qualifier | Meaning | Value |
|---|---|---|
| `P1545` series ordinal | seat number | string: `"1"` … `"n"` |
| `P1352` ranking | precedence, 1 = highest | quantity: `1` … `n` |
| `P155` follows | person in seat n−1 | item / `somevalue` (unnamed person) / `novalue` (end of table) |
| `P156` followed by | person in seat n+1 | same |
| `P461` opposite of | person in the seat across | item / `somevalue` (unnamed) / `novalue` (nobody across) |
| `P3831` object has role | role in this event | e.g. bride, bridegroom; only if the role is specific to the event |
| `P39` position held | office the person sits as | e.g. chamberlain; for unnamed persons always, for named ones if the text says so |
| `P1932` object named as | name/title exactly as in the source | string; optional |

Main value: the person's QID, or `somevalue` when the text gives only an office
or the person has no (unambiguous) item.

Every seat gets `P1545`, `P1352`, `P155`, `P156` and `P461`. Set an
end-of-table seat's outer neighbour to `novalue`, not by leaving it out.

## References

Every referenced statement gets the same block:

```
S248	Q<ZA-Prot n>	S7416	"<folio>"
```

`S248` is the book, not the series. No folio given, only the image number of
the digitised copy → `S958 "Bild <number>"` (section) instead of `S7416`.
Don't repeat the archive URL: it is on the book item.

## Known risk: repeated `somevalue`

QuickStatements adds qualifiers to an **existing** statement if the property
and value match. Two `P710 somevalue` lines may end up merged into one
statement with two `P1545` values. The reference item was built by hand, so
this has not been tested yet.

- After the first run, check on the item that the number of `P710` statements
  equals the number of seats and that each has exactly one `P1545`.
- Merged → fix the item by hand, note it here, and from then on put each
  unnamed seat in its own batch run after the item exists.

## V1 format

One command per line, TAB-separated. New item: `CREATE`, then `LAST` on every
line. Existing item: the QID instead of `LAST`.

```
LAST	<PROPERTY>	<VALUE>	[<QUALIFIER>	<VALUE> ...]	[<SOURCE>	<VALUE> ...]
```

| Kind | Format | Example |
|---|---|---|
| Item | bare id | `Q46242` |
| String / Commons file | quoted | `"8"` |
| Monolingual | `lang:"text"` | `de:"Zeremonialprotokolle"` |
| Time | `+YYYY-MM-DDT00:00:00Z/<precision>` | `+1685-07-15T00:00:00Z/11` |
| Quantity | plain number | `5` |
| Unknown / none | `somevalue` / `novalue` | |
| Label / description / alias | `Lde` / `Dde` / `Ade` + quoted text | `Len	"wedding of …"` |

Precision: `/9` year, `/10` month, `/11` day.

## Example (Q140068424, rebuilt; do not run, the item exists)

Reference block abbreviated as `<REF>` = `S248	Q<ZA-Prot 4>	S7416	"140"`.

```
CREATE
LAST	Len	"wedding of Maximilian II Emanuel, Elector of Bavaria and Maria Antonia, Archduchess of Austria"
LAST	Den	"1685 wedding in Vienna"
LAST	P31	Q63442071
LAST	P276	Q46242	<REF>
LAST	P585	+1685-07-15T00:00:00Z/11	<REF>
LAST	P18	"AT-OeStA-HHStA OMeA ZA-Prot 4 Zeremonialprotokoll (Protocollum Aulicum in Ceremonialibus) 1681 - 1691 (Buch), fol. 140.jpg"
LAST	P1343	Q<ZA-Prot 4>	P7416	"140"
LAST	P710	somevalue	P1545	"1"	P1352	10	P39	Q1138622	P155	novalue	P156	Q29530401	P461	somevalue	<REF>
LAST	P710	Q29530401	P1545	"2"	P1352	8	P39	Q6348379	P155	somevalue	P156	somevalue	P461	somevalue	<REF>
LAST	P710	somevalue	P1545	"3"	P1352	6	P39	Q264323	P155	Q29530401	P156	Q234379	P461	somevalue	<REF>
LAST	P710	Q234379	P1545	"4"	P1352	4	P3831	Q353673	P155	somevalue	P156	Q57527	P461	Q57628	<REF>
LAST	P710	Q57527	P1545	"5"	P1352	2	P155	Q234379	P156	Q150494	P461	novalue	<REF>
LAST	P710	Q150494	P1545	"6"	P1352	1	P155	Q57527	P156	Q237463	P461	novalue	<REF>
LAST	P710	Q237463	P1545	"7"	P1352	3	P155	Q150494	P156	Q57628	P461	novalue	<REF>
LAST	P710	Q57628	P1545	"8"	P1352	5	P3831	Q854830	P155	Q237463	P156	somevalue	P461	Q234379	<REF>
LAST	P710	somevalue	P1545	"9"	P1352	7	P39	Q264323	P155	Q57628	P156	somevalue	P461	somevalue	<REF>
LAST	P710	somevalue	P1545	"10"	P1352	9	P39	Q110620657	P155	somevalue	P156	somevalue	P461	Q29530401	<REF>
LAST	P710	somevalue	P1545	"11"	P1352	11	P39	Q1138622	P155	somevalue	P156	novalue	P461	somevalue	<REF>
```

Seats 5–7 are the head of the table (Empress Eleonore Magdalene, Leopold I,
Dowager Empress Eleonora Gonzaga); nobody sits across from them.

## Report (`<base>.qs-report.md`)

For the person who runs the batch. Leave out empty sections.

```markdown
# QuickStatements report: <event> (<date>)

Source: Zeremonialprotokoll <n> (Q…), fol. <folio>.
Batch: `<base>.qs`, <n> commands. URL in `<base>.qs.url`.

## Table
Seat numbering: <direction, e.g. "left to right from the host's view, as drawn">.

| Seat | Rank | Named as | Item | Role / office |
|---|---|---|---|---|
| 6 | 1 | "Ihre Kays. May." | Leopold I (Q150494) | – |

## Derived, not stated
- Ranks 6–11 derived from the seating order, not given in the text.

## Ambiguous persons
- Seat 9 "Cammerherr Graf Harrach": Q… or Q…; set to somevalue.

## No Wikidata item yet
- …

## Open questions
- …
```
