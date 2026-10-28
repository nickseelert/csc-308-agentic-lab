from analysis import metrics


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
