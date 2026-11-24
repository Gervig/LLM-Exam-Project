## Dataset profile: residential buildings from OpenStreetMap

Source: OpenStreetMap via the Overpass API, residential `building=*` ways, 2175 buildings, bounding box south=55.66, west=12.55, north=55.7, east=12.62. OSM is volunteer-maintained and may be outdated.

Building types: apartments 93%, terrace 2%, semidetached_house 1%, house 1%, detached 1%, dormitory 1%, residential 1%.

## How complete the data is

Share of buildings where the field is filled in. A missing value is not zero.

- building:levels (number of floors): 65% overall (apartment 65%, detached 39%, dormitory 71%, terraced 73%).
- building:flats (number of dwellings): 0% overall (apartment 0%, detached 0%, dormitory 0%, terraced 0%).
- height: 1% overall (apartment 1%, detached 0%, dormitory 0%, terraced 0%).
- roof:levels: 53% overall (apartment 53%, detached 29%, dormitory 36%, terraced 61%).
- footprint area (computed from the geometry): 100% overall (apartment 100%, detached 95%, dormitory 100%, terraced 100%).

The number of dwellings (`building:flats`) is almost never available, so the number of flats is usually unknown. The estimate then has to come from the floor area (footprint x floors).

Information tiers (share of buildings): A 0%, B 65%, C 0%, D 35%, E 0%. A = flats known, B = levels and footprint, C = levels only, D = footprint only, E = type only.
