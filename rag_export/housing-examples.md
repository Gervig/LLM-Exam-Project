# Worked examples: buildings with a reasoned capacity

Capacities below come from the rules in this material, not from measurements. They show how to reason from the data.

## Example 1: apartment, confidence high
housingType: apartment
buildingType: apartments
numberOfLevels: 5
numberOfFlats: 12
heightMeters: unknown
footprintM2: 179
Reasoning: 12 flats x 1.8 persons per dwelling.
capacity: 22
confidence: high

## Example 2: apartment, confidence low
housingType: apartment
buildingType: apartments
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 146
Reasoning: footprint 146 m2 x 5 floors (levels missing, median of the group used) x 0.8 = 583 m2 usable; / 84.5 m2 per dwelling = 7 dwellings x 1.8 persons.
capacity: 13
confidence: low

## Example 3: apartment, confidence low
housingType: apartment
buildingType: apartments
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 158
Reasoning: footprint 158 m2 x 5 floors (levels missing, median of the group used) x 0.8 = 631 m2 usable; / 84.5 m2 per dwelling = 7 dwellings x 1.8 persons.
capacity: 13
confidence: low

## Example 4: apartment, confidence low
housingType: apartment
buildingType: apartments
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 190
Reasoning: footprint 190 m2 x 5 floors (levels missing, median of the group used) x 0.8 = 762 m2 usable; / 84.5 m2 per dwelling = 9 dwellings x 1.8 persons.
capacity: 16
confidence: low

## Example 5: apartment, confidence low
housingType: apartment
buildingType: apartments
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 2333
Reasoning: footprint 2333 m2 x 5 floors (levels missing, median of the group used) x 0.8 = 9334 m2 usable; / 84.5 m2 per dwelling = 110 dwellings x 1.8 persons.
capacity: 198
confidence: low

## Example 6: apartment, confidence low
housingType: apartment
buildingType: apartments
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 3395
Reasoning: footprint 3395 m2 x 5 floors (levels missing, median of the group used) x 0.8 = 13580 m2 usable; / 84.5 m2 per dwelling = 161 dwellings x 1.8 persons.
capacity: 290
confidence: low

## Example 7: apartment, confidence medium
housingType: apartment
buildingType: apartments
numberOfLevels: 5
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 689
Reasoning: footprint 689 m2 x 5 floors x 0.8 = 2755 m2 usable; / 84.5 m2 per dwelling = 33 dwellings x 1.8 persons.
capacity: 59
confidence: medium

## Example 8: apartment, confidence medium
housingType: apartment
buildingType: apartments
numberOfLevels: 3
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 114
Reasoning: footprint 114 m2 x 3 floors x 0.8 = 273 m2 usable; / 84.5 m2 per dwelling = 3 dwellings x 1.8 persons.
capacity: 5
confidence: medium

## Example 9: apartment, confidence medium
housingType: apartment
buildingType: apartments
numberOfLevels: 5
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 1072
Reasoning: footprint 1072 m2 x 5 floors x 0.8 = 4286 m2 usable; / 84.5 m2 per dwelling = 51 dwellings x 1.8 persons.
capacity: 92
confidence: medium

## Example 10: apartment, confidence medium
housingType: apartment
buildingType: apartments
numberOfLevels: 4
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 294
Reasoning: footprint 294 m2 x 4 floors x 0.8 = 940 m2 usable; / 84.5 m2 per dwelling = 11 dwellings x 1.8 persons.
capacity: 20
confidence: medium

## Example 11: apartment, confidence medium
housingType: apartment
buildingType: apartments
numberOfLevels: 5
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 347
Reasoning: footprint 347 m2 x 5 floors x 0.8 = 1386 m2 usable; / 84.5 m2 per dwelling = 16 dwellings x 1.8 persons.
capacity: 29
confidence: medium

## Example 12: detached, confidence low
housingType: house
buildingType: house
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 202
Reasoning: footprint 202 m2 x 1 floors (levels missing, median of the group used) x 0.8 = 162 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: low

## Example 13: detached, confidence low
housingType: house
buildingType: detached
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 96
Reasoning: footprint 96 m2 x 1 floors (levels missing, median of the group used) x 0.8 = 77 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: low

## Example 14: detached, confidence low
housingType: house
buildingType: detached
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 136
Reasoning: footprint 136 m2 x 1 floors (levels missing, median of the group used) x 0.8 = 109 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: low

## Example 15: detached, confidence low
housingType: house
buildingType: detached
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 145
Reasoning: footprint 145 m2 x 1 floors (levels missing, median of the group used) x 0.8 = 116 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: low

## Example 16: detached, confidence low
housingType: house
buildingType: house
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 18
Reasoning: footprint 18 m2 x 1 floors (levels missing, median of the group used) x 0.8 = 14 m2 usable; one dwelling x 2.6 persons; limited to 1 by the 20 m2 per person ceiling.
capacity: 1
confidence: low

## Example 17: detached, confidence medium
housingType: house
buildingType: detached
numberOfLevels: 3
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 283
Reasoning: footprint 283 m2 x 3 floors x 0.8 = 678 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: medium

## Example 18: detached, confidence medium
housingType: house
buildingType: house
numberOfLevels: 1
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 58
Reasoning: footprint 58 m2 x 1 floors x 0.8 = 47 m2 usable; one dwelling x 2.6 persons; limited to 2 by the 20 m2 per person ceiling.
capacity: 2
confidence: medium

## Example 19: detached, confidence medium
housingType: house
buildingType: detached
numberOfLevels: 1
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 169
Reasoning: footprint 169 m2 x 1 floors x 0.8 = 136 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: medium

## Example 20: detached, confidence medium
housingType: house
buildingType: house
numberOfLevels: 1
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 80
Reasoning: footprint 80 m2 x 1 floors x 0.8 = 64 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: medium

## Example 21: detached, confidence medium
housingType: house
buildingType: detached
numberOfLevels: 1
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 140
Reasoning: footprint 140 m2 x 1 floors x 0.8 = 112 m2 usable; one dwelling x 2.6 persons.
capacity: 3
confidence: medium

## Example 22: terraced, confidence low
housingType: house
buildingType: semidetached_house
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 182
Reasoning: footprint 182 m2 x 2 floors (levels missing, median of the group used) x 0.8 = 291 m2 usable; / 93 m2 per dwelling = 3 dwellings x 1.9 persons.
capacity: 6
confidence: low

## Example 23: terraced, confidence low
housingType: house
buildingType: semidetached_house
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 144
Reasoning: footprint 144 m2 x 2 floors (levels missing, median of the group used) x 0.8 = 231 m2 usable; / 93 m2 per dwelling = 2 dwellings x 1.9 persons.
capacity: 4
confidence: low

## Example 24: terraced, confidence low
housingType: house
buildingType: semidetached_house
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 138
Reasoning: footprint 138 m2 x 2 floors (levels missing, median of the group used) x 0.8 = 222 m2 usable; / 93 m2 per dwelling = 2 dwellings x 1.9 persons.
capacity: 4
confidence: low

## Example 25: terraced, confidence low
housingType: house
buildingType: terrace
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 440
Reasoning: footprint 440 m2 x 2 floors (levels missing, median of the group used) x 0.8 = 704 m2 usable; / 93 m2 per dwelling = 8 dwellings x 1.9 persons.
capacity: 15
confidence: low

## Example 26: terraced, confidence low
housingType: house
buildingType: terrace
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 494
Reasoning: footprint 494 m2 x 2 floors (levels missing, median of the group used) x 0.8 = 790 m2 usable; / 93 m2 per dwelling = 8 dwellings x 1.9 persons.
capacity: 15
confidence: low

## Example 27: terraced, confidence medium
housingType: house
buildingType: terrace
numberOfLevels: 2
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 47
Reasoning: footprint 47 m2 x 2 floors x 0.8 = 76 m2 usable; / 93 m2 per dwelling = 1 dwellings x 1.9 persons.
capacity: 2
confidence: medium

## Example 28: terraced, confidence medium
housingType: house
buildingType: terrace
numberOfLevels: 2
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 891
Reasoning: footprint 891 m2 x 2 floors x 0.8 = 1426 m2 usable; / 93 m2 per dwelling = 15 dwellings x 1.9 persons.
capacity: 28
confidence: medium

## Example 29: terraced, confidence medium
housingType: house
buildingType: terrace
numberOfLevels: 2
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 298
Reasoning: footprint 298 m2 x 2 floors x 0.8 = 476 m2 usable; / 93 m2 per dwelling = 5 dwellings x 1.9 persons.
capacity: 10
confidence: medium

## Example 30: terraced, confidence medium
housingType: house
buildingType: terrace
numberOfLevels: 2
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 46
Reasoning: footprint 46 m2 x 2 floors x 0.8 = 74 m2 usable; / 93 m2 per dwelling = 1 dwellings x 1.9 persons.
capacity: 2
confidence: medium

## Example 31: terraced, confidence medium
housingType: house
buildingType: terrace
numberOfLevels: 2
numberOfFlats: unknown
heightMeters: unknown
footprintM2: 46
Reasoning: footprint 46 m2 x 2 floors x 0.8 = 74 m2 usable; / 93 m2 per dwelling = 1 dwellings x 1.9 persons.
capacity: 2
confidence: medium
