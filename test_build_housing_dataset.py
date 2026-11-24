import csv, json, os, tempfile, unittest
import build_housing_dataset as b

def square(lat, lon, side_m):
    # ~side_m metres square around (lat, lon)
    import math
    dlat = math.degrees(side_m / b.EARTH_RADIUS_M)
    dlon = math.degrees(side_m / (b.EARTH_RADIUS_M * math.cos(math.radians(lat))))
    pts = [(lat, lon), (lat, lon + dlon), (lat + dlat, lon + dlon), (lat + dlat, lon), (lat, lon)]
    return [{"lat": a, "lon": c} for a, c in pts]

class Tests(unittest.TestCase):
    def test_query(self):
        q = b.build_query((55.66, 12.55, 55.70, 12.62), 50)
        self.assertIn('way["building"~"^(apartments|house', q)
        self.assertTrue(q.endswith("out tags geom 50;"))

    def test_parsers(self):
        self.assertEqual(b.parse_int("4"), 4)
        self.assertEqual(b.parse_int("4;5"), 4)
        self.assertEqual(b.parse_int("3.5"), 3)
        self.assertIsNone(b.parse_int("many"))
        self.assertIsNone(b.parse_int(None))
        self.assertEqual(b.parse_metres("12.5 m"), 12.5)
        self.assertEqual(b.parse_metres("12,5"), 12.5)
        self.assertIsNone(b.parse_metres("tall"))
        self.assertIsNone(b.parse_metres("0"))

    def test_footprint(self):
        area = b.footprint_m2(square(55.68, 12.58, 20))
        self.assertAlmostEqual(area, 400, delta=2)
        self.assertIsNone(b.footprint_m2(square(55.68, 12.58, 20)[:-1]))  # not closed
        self.assertIsNone(b.footprint_m2([]))

    def test_rows_and_csv(self):
        response = {"elements": [
            {"type": "way", "id": 1, "tags": {"building": "apartments", "building:levels": "5", "building:flats": "20",
                                                "height": "16 m", "addr:street": "Vej", "addr:housenumber": "3"},
             "geometry": square(55.68, 12.58, 30)},
            {"type": "way", "id": 2, "tags": {"building": "detached"}, "geometry": square(55.69, 12.6, 10)},
            {"type": "way", "id": 1, "tags": {"building": "apartments"}, "geometry": []},   # duplicate id
            {"type": "node", "id": 9, "tags": {"building": "house"}},                       # not a way
            {"type": "way", "id": 3},                                                       # no tags
        ]}
        rows = b.rows_from_response(response)
        self.assertEqual([r["osm_id"] for r in rows], [1, 2])
        self.assertEqual(rows[0]["housing_type"], "apartment")
        self.assertEqual((rows[0]["levels"], rows[0]["flats"], rows[0]["height_m"]), (5, 20, 16.0))
        self.assertEqual(rows[0]["street_address"], "Vej 3")
        self.assertEqual(rows[1]["housing_type"], "house")
        self.assertIsNone(rows[1]["levels"])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x", "out.csv")
            b.write_csv(rows, path)
            with open(path, encoding="utf-8") as f:
                read = list(csv.DictReader(f))
            self.assertEqual(list(read[0].keys()), b.COLUMNS)
            self.assertEqual(read[1]["levels"], "")
            self.assertEqual(json.loads(read[0]["tags_json"])["building"], "apartments")
        self.assertIn("2 buildings", b.summary(rows))

    def test_cli_from_json(self):
        with tempfile.TemporaryDirectory() as d:
            raw = os.path.join(d, "raw.json")
            json.dump({"elements": [{"type": "way", "id": 7, "tags": {"building": "house"}, "geometry": square(55.68, 12.58, 12)}]}, open(raw, "w"))
            out = os.path.join(d, "o.csv")
            b.main(["--from-json", raw, "--out", out])
            self.assertEqual(len(list(csv.DictReader(open(out, encoding="utf-8")))), 1)

class TileTests(unittest.TestCase):
    def test_split_bbox(self):
        tiles = b.split_bbox((55.0, 12.0, 56.0, 13.0), 2)
        self.assertEqual(len(tiles), 4)
        self.assertEqual(tiles[0], (55.0, 12.0, 55.5, 12.5))
        self.assertEqual(tiles[3], (55.5, 12.5, 56.0, 13.0))

    def test_fetch_tiled_dedupes_and_warns(self):
        calls = []
        def fake(url, query):
            calls.append(query)
            return {"elements": [{"type": "way", "id": 1, "tags": {"building": "house"}},
                                 {"type": "way", "id": len(calls) + 10, "tags": {"building": "house"}}]}
        result = b.fetch_tiled("x", (55.0, 12.0, 56.0, 13.0), 2, 2, pause=0, fetcher=fake)
        self.assertEqual(len(calls), 4)
        self.assertEqual(sorted(e["id"] for e in result["elements"]), [1, 11, 12, 13, 14])

    def test_count(self):
        orig = b.fetch
        b.fetch = lambda url, query: {"elements": [{"type": "count", "tags": {"nodes": "0", "ways": "4321", "relations": "0", "total": "4321"}}]}
        try:
            self.assertEqual(b.count_buildings("x", (55.0, 12.0, 56.0, 13.0)), 4321)
        finally:
            b.fetch = orig
        self.assertTrue(b.build_count_query((1, 2, 3, 4)).endswith("out count;"))


class RetryTests(unittest.TestCase):
    def setUp(self):
        self.orig_post, self.orig_sleep = b._post, b.time.sleep
        b.time.sleep = lambda s: None

    def tearDown(self):
        b._post, b.time.sleep = self.orig_post, self.orig_sleep

    def _http(self, code):
        import urllib.error
        return urllib.error.HTTPError("u", code, "x", {}, None)

    def test_retries_502_then_succeeds(self):
        calls = []
        def post(url, query, timeout=240):
            calls.append(url)
            if len(calls) < 3:
                raise self._http(502)
            return {"elements": []}
        b._post = post
        self.assertEqual(b.fetch("main", "q", mirrors=[]), {"elements": []})
        self.assertEqual(calls, ["main"] * 3)

    def test_falls_back_to_mirror(self):
        calls = []
        def post(url, query, timeout=240):
            calls.append(url)
            if url == "main":
                raise self._http(503)
            return {"elements": [1]}
        b._post = post
        self.assertEqual(b.fetch("main", "q", retries=2, mirrors=["mirror"]), {"elements": [1]})
        self.assertEqual(calls, ["main", "main", "mirror"])

    def test_bad_query_is_not_retried(self):
        calls = []
        def post(url, query, timeout=240):
            calls.append(url)
            raise self._http(400)
        b._post = post
        with self.assertRaises(Exception):
            b.fetch("main", "q", mirrors=["mirror"])
        self.assertEqual(len(calls), 1)

    def test_all_servers_fail_gives_clear_error(self):
        def post(url, query, timeout=240):
            raise self._http(502)
        b._post = post
        with self.assertRaises(RuntimeError) as ctx:
            b.fetch("main", "q", retries=2, mirrors=["m"])
        self.assertIn("All Overpass servers failed", str(ctx.exception))

    def test_tile_cache_resumes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            calls = []
            def fake(url, query):
                calls.append(query)
                if len(calls) == 3:
                    raise RuntimeError("boom")
                return {"elements": [{"type": "way", "id": 100 + len(calls), "tags": {"building": "house"}}]}
            with self.assertRaises(RuntimeError):
                b.fetch_tiled("x", (55.0, 12.0, 56.0, 13.0), 10, 2, pause=0, fetcher=fake, cache_dir=d)
            self.assertEqual(len(calls), 3)   # two tiles saved, third failed
            calls.clear()
            def fake2(url, query):
                calls.append(query)
                return {"elements": [{"type": "way", "id": 200 + len(calls), "tags": {"building": "house"}}]}
            result = b.fetch_tiled("x", (55.0, 12.0, 56.0, 13.0), 10, 2, pause=0, fetcher=fake2, cache_dir=d)
            self.assertEqual(len(calls), 2)   # only the two missing tiles are fetched
            self.assertEqual(len(result["elements"]), 4)


if __name__ == "__main__":
    unittest.main()
