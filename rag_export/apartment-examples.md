# Worked examples: apartment buildings with a reasoned capacity

The capacities come from the rules in this material, not from measurements. They show how to reason.

## Example 1: flats known
buildingType: apartment building
footprintM2: 179
numberOfLevels: 5
numberOfFlats: 12
heightMeters: unknown
Reasoning: 12 flats x 1.8 persons per flat.
capacity: 22
confidence: high

## Example 2: levels known, flats unknown, footprint known
buildingType: apartment building
footprintM2: 248
numberOfLevels: 3
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 248 m2 x 3 floors x 0.8 = 595 m2 usable; 595 / 40 m2 per person = 14.9.
capacity: 15
confidence: medium

## Example 3: levels known, flats unknown, footprint known
buildingType: apartment building
footprintM2: 170
numberOfLevels: 5
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 170 m2 x 5 floors x 0.8 = 678 m2 usable; 678 / 40 m2 per person = 17.0.
capacity: 17
confidence: medium

## Example 4: levels known, flats unknown, footprint known
buildingType: apartment building
footprintM2: 354
numberOfLevels: 5
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 354 m2 x 5 floors x 0.8 = 1415 m2 usable; 1415 / 40 m2 per person = 35.4.
capacity: 35
confidence: medium

## Example 5: levels known, flats unknown, footprint unknown
buildingType: apartment building
footprintM2: unknown
numberOfLevels: 6
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 317 m2 x 6 floors x 0.8 = 1521 m2 usable; 1521 / 40 m2 per person = 38.0; footprint missing, median footprint 317 m2 used.
capacity: 38
confidence: low

## Example 6: levels unknown, flats unknown, footprint known
buildingType: apartment building
footprintM2: 1757
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 1757 m2 x 5 floors x 0.8 = 7030 m2 usable; 7030 / 40 m2 per person = 175.7; levels missing, median of similar buildings (5) used.
capacity: 176
confidence: low

## Example 7: levels unknown, flats unknown, footprint known
buildingType: apartment building
footprintM2: 200
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 200 m2 x 5 floors x 0.8 = 800 m2 usable; 800 / 40 m2 per person = 20.0; levels missing, median of similar buildings (5) used.
capacity: 20
confidence: low

## Example 8: levels unknown, flats unknown, footprint known
buildingType: apartment building
footprintM2: 348
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 348 m2 x 5 floors x 0.8 = 1392 m2 usable; 1392 / 40 m2 per person = 34.8; levels missing, median of similar buildings (5) used.
capacity: 35
confidence: low

## Example 9: levels unknown, flats unknown, footprint unknown
buildingType: apartment building
footprintM2: unknown
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 317 m2 x 5 floors x 0.8 = 1268 m2 usable; 1268 / 40 m2 per person = 31.7; footprint missing, median footprint 317 m2 used; levels missing, median of similar buildings (5) used.
capacity: 32
confidence: low

## Example 10: levels unknown, flats unknown, footprint unknown
buildingType: apartment building
footprintM2: unknown
numberOfLevels: unknown
numberOfFlats: unknown
heightMeters: unknown
Reasoning: footprint 317 m2 x 5 floors x 0.8 = 1268 m2 usable; 1268 / 40 m2 per person = 31.7; footprint missing, median footprint 317 m2 used; levels missing, median of similar buildings (5) used.
capacity: 32
confidence: low
