import pandas as pd
import pytest

from analysis.load import load_pitches


@pytest.fixture(scope="session")
def pitches() -> pd.DataFrame:
    return load_pitches()


@pytest.fixture
def tiny() -> pd.DataFrame:
    """Hand-built frame so metric tests do not depend on real data."""
    return pd.DataFrame(
        {
            "game_pk": [1, 1, 1, 2],
            "game_date": pd.to_datetime(["2026-10-01"] * 3 + ["2026-10-02"]),
            "description": ["swinging_strike", "foul", "ball", "hit_into_play"],
            "events": [None, None, None, "home_run"],
            "release_speed": [99.0, 98.0, 85.0, 97.0],
            "launch_speed": [None, None, None, 110.2],
        }
    )
