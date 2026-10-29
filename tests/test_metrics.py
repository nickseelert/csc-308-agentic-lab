import pandas as pd
import pytest

from analysis import metrics


def _pa(pitcher, name, pitches, event=None):
    """One plate appearance: one row per pitch, terminal `event` on the last row."""
    last = len(pitches) - 1
    return [
        {
            "pitcher": pitcher,
            "pitcher_name": name,
            "description": description,
            "events": event if i == last else None,
        }
        for i, description in enumerate(pitches)
    ]


@pytest.fixture
def appearances() -> pd.DataFrame:
    """Hand-built pitch rows grouped into completed plate appearances."""
    rows = [
        *_pa(100, "Ace", ["ball", "swinging_strike"], "strikeout"),
        *_pa(100, "Ace", ["foul", "hit_into_play"], "double_play"),
        *_pa(100, "Ace", ["ball", "ball", "swinging_strike"], "strikeout"),
        *_pa(200, "Closer", ["swinging_strike"], "strikeout_double_play"),
        *_pa(200, "Closer", ["hit_into_play"], "field_out"),
        *_pa(300, "Setup", ["ball", "hit_into_play"], "single"),
        *_pa(300, "Setup", ["ball", "ball", "ball", "ball"], "walk"),
        *_pa(500, "Alpha", ["foul", "swinging_strike"], "strikeout"),
        *_pa(400, "Zed", ["swinging_strike"], "strikeout"),
        *_pa(600, "Nix", ["swinging_strike"], "strikeout"),
        *_pa(601, "Nix", ["foul", "swinging_strike"], "strikeout_double_play"),
    ]
    return pd.DataFrame(rows)


def test_whiff_rate_counts_only_swings(tiny):
    # 3 swings (swinging_strike, foul, hit_into_play); 1 whiff. "ball" is not a swing.
    assert metrics.whiff_rate(tiny) == 1 / 3


def test_whiff_rate_with_no_swings(tiny):
    assert metrics.whiff_rate(tiny[tiny["description"] == "ball"]) == 0.0


def test_summary_tiny(tiny):
    s = metrics.summary(tiny)
    assert s["pitches"] == 4
    assert s["games"] == 2
    assert s["home_runs"] == 1
    assert s["max_velo"] == 99.0


def test_velocity_leaders_sorted_and_filtered(pitches):
    leaders = metrics.velocity_leaders(pitches, n=5, min_pitches=25)
    assert 0 < len(leaders) <= 5
    velos = [row["avg_velo"] for row in leaders]
    assert velos == sorted(velos, reverse=True)
    assert all(row["pitches"] >= 25 for row in leaders)


def test_pitch_mix_shares_sum_to_one(pitches):
    mix = metrics.pitch_mix(pitches)
    assert abs(sum(row["share"] for row in mix) - 1) < 0.01


def test_hardest_hit_descending(pitches):
    top = metrics.hardest_hit(pitches, n=10)
    assert len(top) == 10
    assert [r["exit_velo"] for r in top] == sorted((r["exit_velo"] for r in top), reverse=True)


def test_strikeout_leaders_count_appearances_not_pitches(appearances):
    # Ace threw 7 pitches over 3 finished plate appearances.
    leaders = metrics.strikeout_leaders(appearances)
    assert leaders[0] == {"pitcher": "Ace", "strikeouts": 2, "batters_faced": 3}


def test_strikeout_leaders_count_both_strikeout_events(appearances):
    leaders = {row["pitcher"]: row for row in metrics.strikeout_leaders(appearances)}
    assert leaders["Closer"]["strikeouts"] == 1  # strikeout_double_play counts as K


def test_strikeout_leaders_bf_covers_other_completed_appearances(appearances):
    leaders = {row["pitcher"]: row for row in metrics.strikeout_leaders(appearances)}
    assert leaders["Ace"]["batters_faced"] == 3  # two K plus a ground double play
    assert leaders["Closer"]["batters_faced"] == 2  # strikeout DP plus a field out


def test_strikeout_leaders_drop_pitchers_without_strikeouts(appearances):
    names = [row["pitcher"] for row in metrics.strikeout_leaders(appearances)]
    assert "Setup" not in names  # single and walk: finished PAs, zero K


def test_strikeout_leaders_keep_separate_pitcher_identities(appearances):
    rows = [row for row in metrics.strikeout_leaders(appearances) if row["pitcher"] == "Nix"]
    assert len(rows) == 2  # two different pitchers share the name


def test_strikeout_leaders_sort_is_deterministic(appearances):
    leaders = metrics.strikeout_leaders(appearances)
    # K descending, then pitcher name, then pitcher id (the two "Nix" pitchers).
    assert [(row["pitcher"], row["strikeouts"]) for row in leaders] == [
        ("Ace", 2),
        ("Alpha", 1),
        ("Closer", 1),
        ("Nix", 1),
        ("Nix", 1),
        ("Zed", 1),
    ]


def test_strikeout_leaders_returns_plain_ints(appearances):
    for row in metrics.strikeout_leaders(appearances):
        assert type(row["strikeouts"]) is int
        assert type(row["batters_faced"]) is int


def test_strikeout_leaders_limits_rows(appearances):
    leaders = metrics.strikeout_leaders(appearances, n=2)
    assert [row["pitcher"] for row in leaders] == ["Ace", "Alpha"]


def test_strikeout_leaders_empty_input():
    empty = pd.DataFrame({"pitcher": [], "pitcher_name": [], "events": []})
    assert metrics.strikeout_leaders(empty) == []
    unfinished = pd.DataFrame({"pitcher": [1], "pitcher_name": ["Ace"], "events": [None]})
    assert metrics.strikeout_leaders(unfinished) == []
