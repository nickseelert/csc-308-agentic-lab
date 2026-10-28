"""Guards on the committed snapshot itself."""

EXPECTED_ROUNDS = {"F", "D", "L", "W"}


def test_snapshot_loads(pitches):
    assert len(pitches) > 10_000


def test_only_postseason_games(pitches):
    assert set(pitches["game_type"]) <= EXPECTED_ROUNDS


def test_every_player_has_a_name(pitches):
    assert pitches["pitcher_name"].notna().all()
    assert pitches["batter_name"].notna().all()


def test_pitches_are_unique(pitches):
    keys = ["game_pk", "at_bat_number", "pitch_number"]
    assert not pitches.duplicated(subset=keys).any()
