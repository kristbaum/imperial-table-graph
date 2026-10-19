# Participants: lookup and new person items

Read in Step 3. Covers how to identify a participant, when a participant gets a
new Wikidata item, and the `<base>_persons.qs` batch.

## Kaiser und Höfe (KH): first stop for courtiers

[Kaiser und Höfe](https://kaiserhof.geschichte.lmu.de/) (LMU München, ed.
Mark Hengerer and Gerhard Schön) is a person database of the courtiers of the
Austrian Habsburgs in the 16th and 17th centuries, built from court-staff
lists (Hofstaatsverzeichnisse) and payroll books. About 8,800 persons. Use it
for every courtier, chamberlain, Truchsess, Vorschneider, Mundschenk or
councillor in a seating plan, before and alongside Wikidata.

- Record URL: `https://kaiserhof.geschichte.lmu.de/<5-digit id>`, e.g.
  [13156](https://kaiserhof.geschichte.lmu.de/13156) (Ferdinand Ernst Mollard,
  1648–1716, Hofkammerpräsident).
- A record gives: the normalised name (`Surname, Given names`) with variants,
  birth and death dates and places, offices at court (Hofstaat / Hofamt) with
  their years, relatives up to distant cousins with their own KH links, and
  GND / VIAF / ISNI where known.
- Wikidata property: **`P1818` Kaiser und Höfe ID** (string, 5 digits, one
  per item). Its "stated in" item is **`Q107208616`** Kaiser und Höfe.
- Fetch a record with `curl -sL https://kaiserhof.geschichte.lmu.de/<id>` (or
  WebFetch) and read the text. The page is large because of the family tree;
  the offices and identifiers are what you need.
- Finding the record: the site's search is JavaScript-only. Use, in order:
  1. SPARQL for Wikidata items with `P1818` among the candidates (below).
  2. Web search `site:kaiserhof.geschichte.lmu.de <surname>`.
  3. The KH links in the family section of a relative's record (the bride's
     or a known courtier's record often lists the person you need).
  4. Otherwise, ask the user to look the name up on the site and give the ID.

```sparql
# Items already carrying a KH ID, by surname in the label
SELECT ?item ?itemLabel ?kh ?birth ?death WHERE {
  ?item wdt:P1818 ?kh; rdfs:label ?l.
  FILTER(LANG(?l) = "de" && CONTAINS(LCASE(?l), "mollard"))
  OPTIONAL { ?item wdt:P569 ?birth. } OPTIONAL { ?item wdt:P570 ?death. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "de,mul,en". }
}
```

```sparql
# Is this KH record already on Wikidata?
SELECT ?item WHERE { ?item wdt:P1818 "13156". }
```

Spelling differs between the protocol, KH and Wikidata (Mollart / Mollard,
Hoyos / Hoyoß, Frhl. = Fräulein, Frh. = Freiherr). Search on the surname stem
and compare dates and offices, not strings.

## Does the person match?

A KH record or Wikidata item matches a seat when all of these hold:

1. The surname and title (Graf, Freiherr …) fit the protocol's wording.
2. The person was alive and of age at the event date.
3. Nothing contradicts the office in the protocol. Best case: KH lists that
   office (Vorschneider, Truchsess, Kämmerer …) for years around the event.

Two or more records fit equally → `somevalue`, candidates in the report
(the ⛔ in Step 3 still applies).

## When to create a new person item

Create one when the person is identified but has no Wikidata item, **and** at
least one of these external sources describes them:

- a KH record (the normal case),
- a GND record,
- another authority or printed reference with life dates (e.g. Wurzbach,
  a genealogical handbook) that you can cite with a URL.

And the new item can carry, from that source, at least: a full name (given
name + surname), and a birth or a death year.

Do **not** create an item from the protocol text alone. "Vorschneider Frh.
Hoyos" names a family and an office, not a person: without a KH or GND record
pinning down which Hoyos it is, the seat stays `somevalue` + `P39` + `P1932`
and goes under "No Wikidata item yet" in the report.

Before creating, make sure there is no item yet:

1. `search_items` with the KH normalised name, the protocol spelling and the
   name variants KH lists.
2. SPARQL on `P1818` = the KH ID, and on `P227` = the GND ID if KH gives one.
3. An item exists without `P1818` → don't create; add the KH ID to it instead
   (see "Enriching existing items").

## The person item

Everything comes from the KH record (or the other source); nothing from
guesswork. Leave out what the source doesn't give.

| Fact | Command | Ref |
|---|---|---|
| Label | `Lde`, `Len`: given names + surname, as KH normalises them (`Ferdinand Ernst Mollard`) | no |
| Description | `Dde` "österreichischer Hofbeamter (1648–1716)", `Den` "Austrian courtier (1648–1716)"; use the KH headline office if there is one (`Hofkammerpräsident` → "Präsident der Hofkammer") | no |
| Aliases | `Ade`: the protocol spelling and the main KH variants (`Ferdinand Ernst von Mollart`) | no |
| Instance of | `P31 Q5` | no |
| Sex or gender | `P21 Q6581097` male / `Q6581072` female, only if the source makes it clear | yes |
| Birth / death | `P569` / `P570`, `/9` for a year, `/11` for a full date | yes |
| Birth / death place | `P19` / `P20`, only if the place has an item you confirmed | yes |
| KH ID | `P1818 "<id>"` | no |
| GND / VIAF | `P227 "<id>"` / `P214 "<id>"`, as linked from the KH record | no |
| Office | `P39 <office>`, only offices in the fixed-ID table or ones you confirmed, with `P580`/`P582` years if KH gives them | yes |
| Father / mother | `P22` / `P25`, only if that parent has an item already | yes |

Reference block for KH facts:

```
S248	Q107208616	S1818	"<id>"	S813	+<today>T00:00:00Z/11
```

A fact taken from the protocol itself (e.g. "Vorschneider in 1673") gets the
usual protocol reference (`S248 <book> S7416 "<folio>"`) instead.

Example (KH 13156; check for an existing item before running):

```
CREATE
LAST	Lde	"Ferdinand Ernst Mollard"
LAST	Len	"Ferdinand Ernst Mollard"
LAST	Dde	"österreichischer Hofbeamter (1648–1716)"
LAST	Den	"Austrian courtier (1648–1716)"
LAST	Ade	"Ferdinand Ernst von Mollart"
LAST	P31	Q5
LAST	P21	Q6581097	S248	Q107208616	S1818	"13156"	S813	+2026-10-19T00:00:00Z/11
LAST	P569	+1648-00-00T00:00:00Z/9	S248	Q107208616	S1818	"13156"	S813	+2026-10-19T00:00:00Z/11
LAST	P570	+1716-08-08T00:00:00Z/11	S248	Q107208616	S1818	"13156"	S813	+2026-10-19T00:00:00Z/11
LAST	P1818	"13156"
LAST	P227	"1041885512"
LAST	P214	"308205209"
```

## Two batches when new persons are needed

QuickStatements can't refer back to an item created earlier in the batch
(only `LAST` = the newest one), so new persons go in their own batch:

1. `<base>_persons.qs`: one `CREATE` block per new person, plus the
   enrichment lines below. Run it first.
2. `<base>.qs`: the event. Where a new person sits, write the placeholder
   `Q<new: Ferdinand Ernst Mollard>` as the `P710` value and in neighbours'
   `P155`/`P156`/`P461`. `scripts/qs_url.py` refuses files with placeholders,
   so the event batch can't be run by mistake before the persons exist.
3. After the persons batch has run, replace each placeholder with the new QID,
   then run `python3 scripts/qs_url.py batches/<base>.qs`.

Run `qs_url.py` on `<base>_persons.qs` straight away; it has no placeholders.

## Enriching existing items

When a participant already has an item but it lacks the KH ID (or the GND ID
KH gives), add it in `<base>_persons.qs`:

```
Q…	P1818	"<id>"
```

(with the real QID in place of `Q…`).

Only when the match is certain (dates, office and family agree). These lines
merge by value, so re-running them is harmless.

## Report additions

In `<base>.qs-report.md`, add:

```markdown
## New person items (`<base>_persons.qs`)
| Seat | Named as | New item | Source |
|---|---|---|---|
| 6 | "Vorschneider Graf von Mollart" | Ferdinand Ernst Mollard (1648–1716) | KH 13156 |

## KH IDs added to existing items
- Q… ← KH …
```

And in the Table section, give the KH ID next to every participant that has
one.
