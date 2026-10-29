"""Write the JSON files the Next.js site renders at build time.

Usage: python -m analysis.build_site_data [output_dir]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from analysis import metrics
from analysis.load import load_pitches

DEFAULT_OUT = Path(__file__).resolve().parent.parent / "site" / "data"


def build(out_dir: Path = DEFAULT_OUT) -> list[Path]:
    df = load_pitches()
    payloads = {
        "summary.json": metrics.summary(df) | {"whiff_rate": round(metrics.whiff_rate(df), 4)},
        "velocity_leaders.json": metrics.velocity_leaders(df),
        "strikeout_leaders.json": metrics.strikeout_leaders(df),
        "pitch_mix.json": metrics.pitch_mix(df),
        "hardest_hit.json": metrics.hardest_hit(df),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, payload in payloads.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2) + "\n")
        written.append(path)
    return written


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    for p in build(target):
        print(p)
