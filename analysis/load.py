"""Load the committed Statcast snapshot. No network access."""

from __future__ import annotations

from functools import cache
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PITCHES_FILE = DATA_DIR / "postseason_2026.csv.gz"
PLAYERS_FILE = DATA_DIR / "players.csv"

ROUND_NAMES = {
    "F": "Wild Card",
    "D": "Division Series",
    "L": "League Championship",
    "W": "World Series",
}


@cache
def _players() -> dict[int, str]:
    players = pd.read_csv(PLAYERS_FILE)
    return dict(zip(players["player_id"], players["name"], strict=True))


def player_name(player_id: int) -> str:
    """Return "First Last" for an MLBAM id, or the id as text if unknown."""
    return _players().get(int(player_id), str(player_id))


def load_pitches(path: Path = PITCHES_FILE) -> pd.DataFrame:
    """Return one row per pitch, with batter/pitcher names attached.

    `player_name` in raw Statcast is the *pitcher* ("Last, First"). We add explicit
    `pitcher_name` and `batter_name` columns so nobody has to remember that.
    """
    df = pd.read_csv(path, parse_dates=["game_date"])
    names = _players()
    df["pitcher_name"] = df["pitcher"].map(names)
    df["batter_name"] = df["batter"].map(names)
    df["round"] = df["game_type"].map(ROUND_NAMES)
    return df
