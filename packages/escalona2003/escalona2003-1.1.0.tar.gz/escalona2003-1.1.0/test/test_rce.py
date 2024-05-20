import pandas as pd
import pytest

from escalona2003 import pth_clean


@pytest.fixture(scope='module')
def data():
    df = pd.read_csv(pth_clean / "rce.csv", sep=";", comment="#")
    return df


def test_all_zones_are_defined_for_each_stage(data):
    for _, df in data.groupby(['variety', 'year', 'stage']):
        assert len(df) == 8


def test_an_is_bounded(data):
    for an in data['an']:
        assert 0 < an < 0.7


def test_ipar_is_bounded(data):
    for ipar in data['ipar']:
        assert 0 < ipar < 60
