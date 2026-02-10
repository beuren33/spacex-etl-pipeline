import pandas as pd
from src.transform.spacex_transformer import SpaceXTransformer
import pytest


@pytest.fixture
def sample_launches_data():
    return [
        {
            "id": "launch1",
            "name": "Falcon 9 Test",
            "date_utc": "2022-01-01T12:00:00.000Z",
            "success": True,
            "rocket": "rocket1",
        }
    ]


def test_transform_launches(sample_launches_data):

    transformer = SpaceXTransformer()

    transformed_df = transformer.transform_launches(sample_launches_data)

    assert not transformed_df.empty
    assert "year" in transformed_df.columns
    assert transformed_df.iloc[0]["year"] == 2022
    assert transformed_df.iloc[0]["success"] == True
