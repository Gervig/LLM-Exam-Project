## Data profile: apartment buildings in central Copenhagen

Source: OpenStreetMap via the Overpass API, `building=apartments` and `building=residential`, 2044 buildings in a box in central Copenhagen. OSM is volunteer-maintained and may be outdated.

## What is usually missing

- Footprint area (computed from the building outline): available for 100% of the buildings.
- Number of levels (building:levels): available for 65%; a height can replace it, but is given for only 1%.
- Number of flats (building:flats): available for 0% (3 buildings). It is almost always unknown, and a missing value is not zero.
- Roof levels (roof:levels) are only given where levels are given, so they add no information when levels are missing.

Typical buildings: median footprint 317 m2 (middle half 190 to 551 m2), median 5 levels (middle half 4 to 5).

Share of buildings per situation: tier A 0%, tier B 65%, tier C 0%, tier D 35%, tier E 0%.

## Levels by footprint size (used when the number of levels is missing)

A larger footprint usually means more levels. Median number of levels per footprint class in this data:

| Footprint class | Median levels | Buildings with levels |
|---|---|---|
| under 100 m2 | 3 | 54 |
| 100-250 m2 | 5 | 423 |
| 250-500 m2 | 5 | 469 |
| 500-1000 m2 | 5 | 244 |
| over 1000 m2 | 5 | 141 |

## Limitations

- There is no real capacity data. All estimates are reasoned from the building, not measured.
- The data covers central Copenhagen only; other areas may differ.
- Buildings with a footprint under 60 m2 are probably annexes or sheds, and over 3000 m2 may be several buildings or not residential. Use confidence low and say so.
- A back-test on the few buildings with a known flat count found that the area formula underestimated the residents (see the notebook). Treat the result as a typical value, not a maximum.
