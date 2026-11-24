#!/usr/bin/env python3
"""Download residential buildings from OpenStreetMap (Overpass API) into one CSV for the EDA.

Only the Python standard library is used, so it runs with `python build_housing_dataset.py` (or `uv run`).

Examples
  # Central Copenhagen (Smart City's default bounding box), at most 2000 buildings, raw response saved too
  python build_housing_dataset.py --limit 2000 --save-raw data/overpass_raw.json --out data/housing_dataset.csv

  # Split the box into 3 x 3 tiles (up to 3000 buildings per tile) so the limit does not cut the sample off
  python build_housing_dataset.py --tiles 3 --limit 3000 --out data/housing_dataset.csv

  # Only count how many buildings the box holds (no geometry, light on Overpass)
  python build_housing_dataset.py --count-only

  # Re-run the processing on a saved response without calling Overpass again
  python build_housing_dataset.py --from-json data/overpass_raw.json --out data/housing_dataset.csv

The query is the one Smart City's building import should use too, so both sides describe the same buildings:
  way[building~"^(apartments|house|...)$"](south,west,north,east); out tags geom <limit>;
Relations (multipolygon buildings) are not included. Ways only.
"""
import argparse
import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_URL = os.environ.get("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
# Community mirrors, used only if the main server keeps failing (not tested by the author; availability varies).
MIRRORS = ["https://overpass.kumi.systems/api/interpreter", "https://overpass.private.coffee/api/interpreter"]
RETRY_STATUS = (429, 500, 502, 503, 504)   # busy or overloaded: wait and try again

# Smart City's default bounding box (SeedController): central Copenhagen.
DEFAULT_BBOX = (55.66, 12.55, 55.70, 12.62)  # south, west, north, east

BUILDING_VALUES = ["apartments", "house", "detached", "semidetached_house", "terrace", "residential",
                   "dormitory", "bungalow"]
# Smart City only knows two housing types. Mapping used for the `housing_type` column.
HOUSE_TYPES = {"house", "detached", "semidetached_house", "terrace", "bungalow"}

COLUMNS = ["osm_type", "osm_id", "building", "housing_type", "levels", "flats", "height_m", "roof_levels",
           "footprint_m2", "node_count", "lat", "lon", "name", "street_address", "tags_json"]

EARTH_RADIUS_M = 6371000.0


def build_query(bbox, limit, timeout=180):
    south, west, north, east = bbox
    values = "|".join(BUILDING_VALUES)
    return (f'[out:json][timeout:{timeout}];'
            f'way["building"~"^({values})$"]({south},{west},{north},{east});'
            f'out tags geom {limit};')


def build_count_query(bbox, timeout=120):
    south, west, north, east = bbox
    values = "|".join(BUILDING_VALUES)
    return (f'[out:json][timeout:{timeout}];'
            f'way["building"~"^({values})$"]({south},{west},{north},{east});out count;')


def count_buildings(url, bbox):
    """Number of matching building ways in the box (Overpass `out count`)."""
    response = fetch(url, build_count_query(bbox))
    for element in response.get("elements", []):
        if element.get("type") == "count":
            return int(element["tags"]["ways"])
    raise RuntimeError("Overpass answer has no count element")


def split_bbox(bbox, n):
    """Split a (south, west, north, east) box into n x n equal tiles."""
    south, west, north, east = bbox
    tiles = []
    for i in range(n):
        for j in range(n):
            tiles.append((round(south + (north - south) * i / n, 6), round(west + (east - west) * j / n, 6),
                          round(south + (north - south) * (i + 1) / n, 6), round(west + (east - west) * (j + 1) / n, 6)))
    return tiles


def fetch_tiled(url, bbox, limit_per_tile, tiles, pause=5, fetcher=None, cache_dir=None):
    """Fetch tile by tile (one request per tile, with a pause) and merge. Buildings on a tile border appear once.
    With cache_dir, every finished tile is saved there and reused on the next run, so a failure halfway
    only costs the tiles that are missing."""
    fetcher = fetcher or fetch
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
    total = tiles * tiles
    merged, seen = [], set()
    for index, tile in enumerate(split_bbox(bbox, tiles), 1):
        cache_file = os.path.join(cache_dir, f"tile_{index}_of_{total}_limit{limit_per_tile}.json") if cache_dir else None
        if cache_file and os.path.exists(cache_file):
            with open(cache_file, encoding="utf-8") as handle:
                response = json.load(handle)
            print(f"Tile {index}/{total}: read from {cache_file}", file=sys.stderr)
            fresh = False
        else:
            response = fetcher(url, build_query(tile, limit_per_tile))
            if cache_file:
                with open(cache_file, "w", encoding="utf-8") as handle:
                    json.dump(response, handle)
            print(f"Tile {index}/{total}: downloaded", file=sys.stderr)
            fresh = True
        got = [e for e in response.get("elements", []) if e.get("type") == "way"]
        if len(got) >= limit_per_tile:
            print(f"Tile {index}/{total} returned the limit ({limit_per_tile}): it may be cut off. "
                  "Use more tiles or a higher limit.", file=sys.stderr)
        for element in got:
            if element["id"] not in seen:
                seen.add(element["id"])
                merged.append(element)
        if fresh and index < total and pause:
            time.sleep(pause)
    return {"elements": merged}


def _post(url, query, timeout=240):
    body = urllib.parse.urlencode({"data": query}).encode()
    request = urllib.request.Request(url, data=body, headers={
        "User-Agent": "smart-city-exam-dataset/1.0 (school project)",
        "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def fetch(url, query, retries=4, pause=15, mirrors=None):
    """POST the query. Busy or overloaded answers (429, 5xx) and timeouts are retried with a growing pause,
    then the mirrors are tried. Other errors (for example 400 = bad query) are raised at once."""
    mirrors = MIRRORS if mirrors is None else mirrors
    last_error = None
    for server in [url] + [m for m in mirrors if m != url]:
        for attempt in range(1, retries + 1):
            try:
                return _post(server, query)
            except urllib.error.HTTPError as error:
                last_error = error
                if error.code not in RETRY_STATUS:
                    raise
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                last_error = error
            if attempt < retries:
                wait = pause * attempt
                print(f"{server}: {last_error}. Waiting {wait}s (try {attempt}/{retries}) ...", file=sys.stderr)
                time.sleep(wait)
        print(f"{server} keeps failing, trying the next server.", file=sys.stderr)
    raise RuntimeError(f"All Overpass servers failed. Last error: {last_error}. "
                       "Check https://overpass-api.de/api/status, wait a few minutes, or use more tiles with a lower limit.")


def parse_int(value):
    """'4' -> 4, '4;5' -> 4 (first value), '3.5' -> 3, junk -> None."""
    if value is None:
        return None
    first = str(value).split(";")[0].strip()
    try:
        return int(float(first))
    except ValueError:
        return None


def parse_metres(value):
    """'12' -> 12.0, '12.5 m' -> 12.5, '12,5' -> 12.5, junk -> None."""
    if value is None:
        return None
    text = str(value).split(";")[0].strip().lower().replace("metres", "").replace("meters", "")
    text = text.replace("m", "").replace(",", ".").strip()
    try:
        number = float(text)
    except ValueError:
        return None
    return number if number > 0 else None


def footprint_m2(geometry):
    """Area of the closed way in square metres (shoelace on a local flat projection). None if not a closed polygon."""
    if not geometry or len(geometry) < 4:
        return None
    first, last = geometry[0], geometry[-1]
    if first["lat"] != last["lat"] or first["lon"] != last["lon"]:
        return None
    lat0 = math.radians(sum(p["lat"] for p in geometry) / len(geometry))
    points = [(EARTH_RADIUS_M * math.radians(p["lon"]) * math.cos(lat0),
               EARTH_RADIUS_M * math.radians(p["lat"])) for p in geometry]
    area = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def street_address(tags):
    street, number = tags.get("addr:street"), tags.get("addr:housenumber")
    if street and number:
        return f"{street} {number}"
    return street or number or ""


def to_row(element):
    tags = element.get("tags", {})
    geometry = element.get("geometry", [])
    building = tags.get("building", "")
    area = footprint_m2(geometry)
    if geometry:
        lat = sum(p["lat"] for p in geometry) / len(geometry)
        lon = sum(p["lon"] for p in geometry) / len(geometry)
    else:
        lat = lon = None
    return {
        "osm_type": element.get("type", "way"),
        "osm_id": element["id"],
        "building": building,
        "housing_type": "house" if building in HOUSE_TYPES else "apartment",
        "levels": parse_int(tags.get("building:levels")),
        "flats": parse_int(tags.get("building:flats")),
        "height_m": parse_metres(tags.get("height")),
        "roof_levels": parse_int(tags.get("roof:levels")),
        "footprint_m2": None if area is None else round(area, 1),
        "node_count": max(len(geometry) - 1, 0),
        "lat": None if lat is None else round(lat, 6),
        "lon": None if lon is None else round(lon, 6),
        "name": tags.get("name", ""),
        "street_address": street_address(tags),
        "tags_json": json.dumps(tags, ensure_ascii=False, sort_keys=True),
    }


def rows_from_response(response):
    seen, rows = set(), []
    for element in response.get("elements", []):
        if element.get("type") != "way" or "tags" not in element:
            continue
        key = (element["type"], element["id"])
        if key in seen:
            continue
        seen.add(key)
        rows.append(to_row(element))
    return rows


def write_csv(rows, path):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def summary(rows):
    total = len(rows)
    if not total:
        return "No buildings found."
    def filled(name):
        return sum(1 for r in rows if r[name] not in (None, ""))
    lines = [f"{total} buildings"]
    for name in ("levels", "flats", "height_m", "roof_levels", "footprint_m2", "street_address"):
        lines.append(f"  {name:15s} {filled(name):6d}  ({100 * filled(name) / total:.0f}%)")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bbox", nargs=4, type=float, metavar=("SOUTH", "WEST", "NORTH", "EAST"),
                        default=DEFAULT_BBOX, help="default: central Copenhagen, like Smart City")
    parser.add_argument("--limit", type=int, default=1000, help="maximum number of buildings per request/tile (default 1000)")
    parser.add_argument("--tiles", type=int, default=1, help="split the box into N x N tiles, one request each (default 1)")
    parser.add_argument("--count-only", action="store_true", help="only print how many buildings the box holds")
    parser.add_argument("--url", default=DEFAULT_URL, help="Overpass endpoint (default: OVERPASS_URL or overpass-api.de)")
    parser.add_argument("--out", default="data/housing_dataset.csv")
    parser.add_argument("--save-raw", help="also save the raw Overpass response to this file")
    parser.add_argument("--from-json", help="read a saved Overpass response instead of calling Overpass")
    args = parser.parse_args(argv)

    if args.count_only:
        print(f"{count_buildings(args.url, tuple(args.bbox))} building ways in the box")
        return
    if args.from_json:
        with open(args.from_json, encoding="utf-8") as handle:
            response = json.load(handle)
    else:
        if args.tiles > 1:
            response = fetch_tiled(args.url, tuple(args.bbox), args.limit, args.tiles,
                                   cache_dir=os.path.join(os.path.dirname(os.path.abspath(args.out)), "tiles"))
        else:
            response = fetch(args.url, build_query(tuple(args.bbox), args.limit))
        if args.save_raw:
            os.makedirs(os.path.dirname(os.path.abspath(args.save_raw)), exist_ok=True)
            with open(args.save_raw, "w", encoding="utf-8") as handle:
                json.dump(response, handle)
    rows = rows_from_response(response)
    write_csv(rows, args.out)
    print(summary(rows))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
