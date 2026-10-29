import json

from analysis.build_site_data import build


def test_build_writes_valid_json(tmp_path):
    written = build(tmp_path)
    assert {p.name for p in written} >= {
        "summary.json",
        "velocity_leaders.json",
        "strikeout_leaders.json",
    }
    for path in written:
        json.loads(path.read_text())
