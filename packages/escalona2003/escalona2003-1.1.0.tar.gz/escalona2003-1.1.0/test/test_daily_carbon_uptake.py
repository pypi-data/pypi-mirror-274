import pandas as pd
import pytest

from escalona2003 import pth_clean


@pytest.fixture(scope='module')
def data():
    df = pd.read_csv(pth_clean / "daily_carbon_uptake.csv", sep=";", comment="#")
    return df


def test_all_zones_are_defined_for_each_stage(data):
    for _, df in data.groupby(['variety', 'year', 'stage']):
        assert len(df) == 8
        assert set(df['zone']) == {1, 2, 3, 4, 5, 6, 7, 8}


def test_carbon_uptake_is_bounded(data):
    for uptake in data['photo_net']:
        assert 0 < uptake < 8
