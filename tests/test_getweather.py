from getweather import __version__
from getweather import getweather

import pytest

def test_version():
    assert __version__ == '0.1.0'

def test_CityInfo():
    expected=833.0
    a=getweather.CityInfo()
    actual=a.iloc[0,0]
    assert actual==expected

def test_CityId():
    example='Taglag'
    actual=getweather.CityId(example)
    expected=3245
    assert actual==expected

def test_CityCoord():
    example='Taglag'
    actual=getweather.CityCoord(example)
    expected=(44.98333, 38.450001)
    assert actual==expected

def test_CityIds():
    actual=getweather.CityIds('London','Shanghai','New York')
    expected='2643743,1796236,5128638'
    assert actual==expected
    