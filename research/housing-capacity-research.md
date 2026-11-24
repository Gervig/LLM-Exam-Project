# Housing capacity: research findings

Research for the Smart City `HOUSING_CAPACITY` estimate (LLM exam). Written 24 November 2026.

**Question:** how many residents can a residential building hold, when the only data is what OpenStreetMap (OSM) has
(footprint, number of levels, sometimes height)? Two things are needed: typical figures to turn floor area into residents,
and legal limits that work as an upper bound.

**Reliability.** Statistics come from Danmarks Statistik (DST) pages, read directly. The 2026 dwelling sizes are quoted by
Bolius, which cites Statistikbanken table BOL106; I could not query BOL106 itself. The legal texts were read on summary sites
(lovguiden.dk, danskelove.dk, nyidanmark.dk), not on retsinformation.dk. I am not a lawyer. Check the legal points and the
BOL106 figures at the primary source before they go in the synopsis.

## 1. Typical figures (statistics, not rules)

| Figure | Value | Date | Source |
|---|---|---|---|
| Average floor area per person, Denmark | 53.9 m² | 2026 | [DST, Personer i boliger](https://www.dst.dk/da/Statistik/emner/borgere/boligforhold/personer-i-boliger) |
| Floor area per person, Copenhagen municipality | about 40 m² | 1 Jan 2016 | [DST, Nyt nr. 164](https://www.dst.dk/nyt/21543) |
| Floor area per person by household size | 1 person 84-85 m², 2 persons 60 m², 3 persons 42-43 m², 4 persons 36 m² | 2016 and 2020 | [DST, Nyt nr. 164](https://www.dst.dk/nyt/21543), [DST, Nyt 2020](https://www.dst.dk/nyt/30704) |
| Persons per dwelling, Denmark | 2.1 | 1 Jan 2020 | [DST, "Lidt flere end to personer pr. bolig"](https://www.dst.dk/nyt/30704) |
| Persons per dwelling, apartments (etageboliger) | 1.8 | 1 Jan 2020 | same |
| Persons per dwelling, detached houses (parcel-/stuehuse) | 2.6 | 1 Jan 2020 | same |
| Persons per dwelling, terraced, chain and semi-detached houses | 1.9 | 1 Jan 2020 | same |
| Average apartment size, Denmark | 79.1 m² | 2026 | Statistikbanken BOL106, quoted by [Bolius](https://www.bolius.dk/danskerne-faar-mere-og-mere-plads-i-boligen-36883) |
| Average apartment size, Copenhagen city | 84.5 m² | 2026 | same |
| Average detached house size | 155.3 m² | 2026 | same |
| Average terraced, chain and semi-detached house size | 93 m² | 1 Jan 2016 | [DST, Nyt nr. 164](https://www.dst.dk/nyt/21543) |

Notes:

- The 2016 and 2020 figures are older than the 2026 ones. For apartments the check is consistent: 84.5 m² per dwelling / 1.8 persons
  is about 47 m² per person, between the Copenhagen figure (about 40 m², 2016) and the national one (53.9 m², 2026).
- DST also publishes the data in Statistikbanken: BOL106 (area per person over time), BOL201 (persons by dwelling type) and BOL203
  (persons by tenure and region), named on the [Personer i boliger](https://www.dst.dk/da/Statistik/emner/borgere/boligforhold/personer-i-boliger) page.
  A Copenhagen-specific figure for persons per apartment could be taken from there.

## 2. Legal limits (upper bounds, not typical occupancy)

| Rule | Content | Source |
|---|---|---|
| Maximum per room (rental housing) | A rental unit may not be let to or lived in by more than **2 persons per habitable room** (`beboelsesrum`). Applies to an apartment or a single room. Exceptions: household growth through the tenant's children, spouse or partner (or their children), or municipal permission. | [Lov om boligforhold § 14](https://www.lovguiden.dk/loven/lov-om-boligforhold/14,15,17); earlier wording: [Boligreguleringsloven § 52 a](https://danskelove.dk/boligreguleringsloven/52a) |
| Municipal permission | The municipality may allow more than 2 persons per room for ill or elderly relatives needing care, for other pressing social reasons, or when the dwelling has **at least 20 m² per person** after the increase. | [Lov om boligforhold § 15](https://www.lovguiden.dk/loven/lov-om-boligforhold/14,15,17) |
| Control | The municipality may cross-check the person register (CPR) against the building and dwelling register (BBR). | [Lov om boligforhold § 17](https://www.lovguiden.dk/loven/lov-om-boligforhold/14,15,17) |
| Family reunification housing requirement | The residence must have **no more than 2 persons per room, or at least 20 m² of residential area per person**. Example on the page: a 60 m² one-room flat is enough for up to 3 people. | [nyidanmark.dk](https://nyidanmark.dk/en-GB/Words-and-concepts/US/Familie/Family-reunification---Independent-reasonably-sized-residence) |
| Building regulations (BR18, chapter 9) | The dwelling-layout guidance I could read contains no occupancy limit and no minimum dwelling area. It refers to BR18 §§ 196-241 and SBi-anvisning 272 and 249 for specifics. | [BR18 guidance on dwelling layout](https://www.bygningsreglementet.dk/media/mxyjuv0r/boligindretning.pdf) |

Notes:

- I found no general Danish rule that fixes a maximum number of residents from floor area alone. The two area and room tests above
  apply to rental housing and to the family-reunification requirement.
- The room test cannot be used with OSM data, which has no room count. The 20 m² per person figure is the only area-based limit, so
  the baseline uses it as a **ceiling** (usable area / 20), never as the estimate. Real occupancy is about 40-54 m² per person.
- Whether the rule applies to owner-occupied homes was not established from these sources.

## 3. How the findings are used in the baseline

1. Usable area = footprint x floors x an efficiency factor (**0.8, an assumption with no source**).
2. Dwellings = usable area / average dwelling size (apartments 84.5 m², terraced 93 m²; a detached house counts as one dwelling).
3. Capacity = dwellings x persons per dwelling (1.8, 1.9 or 2.6 by type), at least 1.
4. Capacity is capped at usable area / 20 m².
5. Dormitories get no baseline: their capacity is rooms, not flats.

## 4. Gaps and next checks

- Check BOL106 in Statistikbanken directly for the 2026 apartment and house sizes, and look up the Copenhagen figure for persons per apartment.
- Read the legal paragraphs on [retsinformation.dk](https://www.retsinformation.dk) to confirm the wording and the current law. I did not read it there.
- The efficiency factor (0.8) is unsourced. The notebook has a sensitivity table (section 6.2) for it.
- No real capacity data exists for the buildings. The baseline is a documented rule, not ground truth, and the evaluation needs hand-labelled buildings.
- Not looked at: the building and dwelling register (BBR). It holds the number of dwellings and floor areas per building, which would
  replace the OSM guesses, but I did not check how it can be accessed.

## Sources

- Danmarks Statistik, Personer i boliger: <https://www.dst.dk/da/Statistik/emner/borgere/boligforhold/personer-i-boliger>
- Danmarks Statistik, "Lidt flere end to personer pr. bolig" (17 April 2020): <https://www.dst.dk/nyt/30704>
- Danmarks Statistik, "På øerne er der god plads" (Nyt nr. 164, 7 April 2016): <https://www.dst.dk/nyt/21543>
- Bolius, "Danskerne får mere og mere plads i boligen": <https://www.bolius.dk/danskerne-faar-mere-og-mere-plads-i-boligen-36883>
- Lov om boligforhold §§ 14, 15 and 17 (lovguiden.dk): <https://www.lovguiden.dk/loven/lov-om-boligforhold/14,15,17>
- Boligreguleringsloven § 52 a (danskelove.dk): <https://danskelove.dk/boligreguleringsloven/52a>
- Ny i Danmark, "Family reunification - Independent reasonably sized residence": <https://nyidanmark.dk/en-GB/Words-and-concepts/US/Familie/Family-reunification---Independent-reasonably-sized-residence>
- Bygningsreglementet 2018, guidance on dwelling layout: <https://www.bygningsreglementet.dk/media/mxyjuv0r/boligindretning.pdf>
