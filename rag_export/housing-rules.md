## Figures from the OpenStreetMap data

These figures describe the buildings in this dataset (central Copenhagen). They are not statistics about the whole country.

- Footprint, apartment: median 317 m2 (middle half 190 to 551), from n=2041 buildings.
- Footprint, detached: median 118 m2 (middle half 77 to 171), from n=36 buildings.
- Footprint, dormitory: not enough buildings in the data (n=14, need 30); no figure derived.
- Footprint, terraced: median 166 m2 (middle half 62 to 304), from n=79 buildings.
- Number of floors, apartment: median 5 floors (middle half 4 to 5), from n=1322 buildings.
- Number of floors, detached: not enough buildings in the data (n=15, need 30); no figure derived.
- Number of floors, dormitory: not enough buildings in the data (n=10, need 30); no figure derived.
- Number of floors, terraced: median 2 floors (middle half 2 to 3), from n=58 buildings.

## Reference figures from Danmarks Statistik

- Average apartment size, Copenhagen city: 84.5 m2 (2026, Statistikbanken BOL106, quoted by Bolius).
- Average detached house size: 155.3 m2 (2026, BOL106, quoted by Bolius).
- Average terraced or semi-detached house size: 93 m2 (1 January 2016, Danmarks Statistik Nyt nr. 164, https://www.dst.dk/nyt/21543).
- Persons per dwelling in 2020: apartments 1.8, detached houses 2.6, terraced and semi-detached houses 1.9 (https://www.dst.dk/nyt/30704).
- Average floor area per person in Denmark: 53.9 m2 in 2026 (https://www.dst.dk/da/Statistik/emner/borgere/boligforhold/personer-i-boliger). For Copenhagen municipality about 40 m2 in 2016.

## Legal limits (upper bounds, not typical occupancy)

- Rental housing: at most 2 persons per habitable room (Lov om boligforhold, paragraph 14).
- The municipality may allow more if the dwelling has at least 20 m2 per person (paragraph 15). The same two tests are used for the family reunification housing requirement.
- The number of rooms is not available in OpenStreetMap, so only the 20 m2 per person limit can be applied. It is used as a ceiling, never as the estimate.

## Assumptions used for capacity (not sourced)

- Share of footprint x floors that is dwelling area: 0.8 (walls, stairs and shops are not dwelling area).
- Roof levels count as 0 of a floor.
- A height is turned into floors with 3 m per floor when the number of floors is missing; when both are missing the median of the building group is used and the confidence is low.
- There is no real capacity data. Estimates are reasoned from the building, not measured.

## Which rule to use

1. Number of flats known: capacity = flats x persons per dwelling for the building type, confidence high.
2. Apartment or terraced building with footprint and floors: usable area = footprint x floors x share; dwellings = usable area / average dwelling size; capacity = dwellings x persons per dwelling; confidence medium.
3. Detached house: one dwelling, capacity = persons per dwelling for detached houses (floor area only limits it).
4. Floors missing: use the median number of floors of the building type and say so; confidence low.
5. Always limit the capacity to usable area / 20 m2, and never return less than 1.
6. Dormitories: capacity is rooms, not flats; say that no reliable estimate is possible.
7. Nothing but the type known: give a conservative estimate, confidence low, and say that the data is missing.
