"""Pure functions over a pitch-level DataFrame. Every function here has a test."""

from __future__ import annotations

import pandas as pd

SWINGS = {
    "swinging_strike",
    "swinging_strike_blocked",
    "foul",
    "foul_tip",
    "hit_into_play",
    "foul_bunt",
    "missed_bunt",
}
WHIFFS = {"swinging_strike", "swinging_strike_blocked", "foul_tip", "missed_bunt"}


def summary(df: pd.DataFrame) -> dict:
    """Headline numbers for the whole snapshot."""
    return {
        "pitches": int(len(df)),
        "games": int(df["game_pk"].nunique()),
        "first_date": df["game_date"].min().date().isoformat(),
        "last_date": df["game_date"].max().date().isoformat(),
        "home_runs": int((df["events"] == "home_run").sum()),
        "strikeouts": int((df["events"] == "strikeout").sum()),
        "max_velo": round(float(df["release_speed"].max()), 1),
        "max_exit_velo": round(float(df["launch_speed"].max()), 1),
    }


def whiff_rate(df: pd.DataFrame) -> float:
    """Whiffs per swing. Returns 0.0 when there are no swings."""
    swings = df["description"].isin(SWINGS).sum()
    if swings == 0:
        return 0.0
    return float(df["description"].isin(WHIFFS).sum() / swings)


def velocity_leaders(df: pd.DataFrame, n: int = 10, min_pitches: int = 25) -> list[dict]:
    """Pitchers ranked by average four-seam fastball velocity."""
    ff = df[df["pitch_type"] == "FF"].dropna(subset=["release_speed"])
    grouped = ff.groupby(["pitcher", "pitcher_name"])["release_speed"].agg(["mean", "max", "size"])
    grouped = grouped[grouped["size"] >= min_pitches].sort_values("mean", ascending=False).head(n)
    return [
        {
            "pitcher": name,
            "avg_velo": round(float(row["mean"]), 1),
            "max_velo": round(float(row["max"]), 1),
            "pitches": int(row["size"]),
        }
        for (_, name), row in grouped.iterrows()
    ]


def pitch_mix(df: pd.DataFrame) -> list[dict]:
    """Share of each pitch type across the whole snapshot, largest first."""
    named = df.dropna(subset=["pitch_name"])
    counts = named["pitch_name"].value_counts()
    total = int(counts.sum())
    return [
        {"pitch": str(pitch), "count": int(count), "share": round(count / total, 4)}
        for pitch, count in counts.items()
    ]


def hardest_hit(df: pd.DataFrame, n: int = 10) -> list[dict]:
    """Top batted balls by exit velocity."""
    balls = df.dropna(subset=["launch_speed"]).sort_values("launch_speed", ascending=False).head(n)
    return [
        {
            "batter": row["batter_name"],
            "exit_velo": round(float(row["launch_speed"]), 1),
            "launch_angle": None if pd.isna(row["launch_angle"]) else int(row["launch_angle"]),
            "result": None if pd.isna(row["events"]) else str(row["events"]).replace("_", " "),
            "date": row["game_date"].date().isoformat(),
            "round": row["round"],
        }
        for _, row in balls.iterrows()
    ]
