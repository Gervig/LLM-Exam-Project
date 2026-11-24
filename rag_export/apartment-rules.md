# Rules for estimating the capacity of an apartment building

Pick the rule whose heading matches what is known about the building. Answer with one JSON object: capacity (whole number, at least 1), confidence, reasoning.

## Rule A: flats known

The number of flats is given. capacity = flats x 1.8 persons per flat, rounded. Confidence high. Levels and footprint can be ignored.

## Rule B: levels known, flats unknown, footprint known

usable area = footprint x levels x 0.8. capacity = usable area / 40 m2 per person, rounded, at least 1 and at most usable area / 20. Confidence medium. If a height is given instead of levels, levels = height / 3 m, rounded.

## Rule C: levels known, flats unknown, footprint unknown

The footprint is missing. Use the median footprint of apartment buildings in this data, 317 m2, then apply rule B. Confidence low. State that the footprint was assumed.

## Rule D: levels unknown, flats unknown, footprint known

The number of levels is missing. Take the median levels for the footprint class from the table in the data profile (for example 5 levels for 250-500 m2), then apply rule B. Confidence low. State that the levels were assumed.

## Rule E: levels unknown, flats unknown, footprint unknown

Almost nothing is known. Give the typical capacity of an apartment building in this data, about 31 residents, with confidence low, and say that the building data is missing.

## Rule F: flagged buildings (very small or very large footprint)

A footprint under 60 m2 is probably an annex or shed, and over 3000 m2 may be several buildings or not residential. Apply the matching rule but use confidence low and mention the unusual size.

## Answer format

Answer with one JSON object and nothing else: {"capacity": 54, "confidence": "medium", "reasoning": "footprint 630 m2 x 5 levels x 0.8 = 2520 m2 usable, / 40 m2 per person = 63"}. Confidence is high, medium or low as stated in the rule. The reasoning names the numbers used and every value that was assumed.
