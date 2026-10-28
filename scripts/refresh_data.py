"""Re-download the Statcast snapshot with pybaseball. Needs network; never run in CI.

Usage: pip install -e ".[refresh]" && python scripts/refresh_data.py 2026-09-29 2026-11-05
"""

from __future__ import annotations

import sys
from pathlib import Path

from pybaseball import playerid_reverse_lookup, statcast

DATA = Path(__file__).resolve().parent.parent / "data"
COLUMNS = [
    "game_pk",
    "game_date",
    "game_type",
    "home_team",
    "away_team",
    "inning",
    "inning_topbot",
    "at_bat_number",
    "pitch_number",
    "pitcher",
    "batter",
    "player_name",
    "stand",
    "p_throws",
    "pitch_type",
    "pitch_name",
    "release_speed",
    "release_spin_rate",
    "pfx_x",
    "pfx_z",
    "plate_x",
    "plate_z",
    "zone",
    "description",
    "events",
    "type",
    "balls",
    "strikes",
    "outs_when_up",
    "launch_speed",
    "launch_angle",
    "hit_distance_sc",
    "bb_type",
    "estimated_woba_using_speedangle",
    "woba_value",
    "delta_run_exp",
    "bat_score",
    "fld_score",
]


def main(start: str, end: str) -> None:
    df = statcast(start_dt=start, end_dt=end, verbose=False)
    df = df[df["game_type"].isin(["F", "D", "L", "W"])][COLUMNS]
    df = df.sort_values(["game_date", "game_pk", "at_bat_number", "pitch_number"])
    df.to_csv(DATA / "postseason_2026.csv.gz", index=False, compression="gzip")

    ids = sorted(set(df["batter"]) | set(df["pitcher"]))
    lookup = playerid_reverse_lookup(ids, key_type="mlbam")
    lookup["name"] = lookup["name_first"].str.title() + " " + lookup["name_last"].str.title()
    players = lookup[["key_mlbam", "name"]].rename(columns={"key_mlbam": "player_id"})
    players.sort_values("player_id").to_csv(DATA / "players.csv", index=False)
    print(f"{len(df)} pitches, {len(players)} players")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
