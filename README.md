# getweather 

![](https://github.com/SijiaChen0110/getweather/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/SijiaChen0110/getweather/branch/main/graph/badge.svg)](https://codecov.io/gh/SijiaChen0110/getweather) ![Release](https://github.com/SijiaChen0110/getweather/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/getweather/badge/?version=latest)](https://getweather.readthedocs.io/en/latest/?badge=latest)

An API client python package for OpenWeatherMap.

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ getweather
```

## Features

- TODO

## Dependencies

- pandas
- matplotlib
- pytest
- os
- requests
- json
- time
- importlib

## Usage
from getweather import getwa=eather

- 1. Get current weather data for one location.
     getweather.getonecity(weather_api_key,'London',status='current')
     
- 2. Get forecast weather data for one location.
     getweather.getonecity(weather_api_key,'London',status='forecast')
     
- 3. Get current weather data for any number of cities you want.
     getweather.getcities(weather_api_key,'London','Shanghai','New York')
     
- 4. Get current weather data from cities laid within a definite circle that is specified by center point (city that you input) and expected number of cities (cnt) around this        point.
     getweather.getcitycircle(weather_api_key,'Shanghai', 20)

## Documentation

The official documentation is hosted on Read the Docs: https://getweather.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/SijiaChen0110/getweather/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
