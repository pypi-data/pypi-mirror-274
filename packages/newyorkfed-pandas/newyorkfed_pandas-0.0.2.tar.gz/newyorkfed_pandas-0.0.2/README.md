# newyorkfed_pandas.py

Library for downloading data from markets.newyorkfed.org API.

The first time you request data, the data is retrieved and saved locally. Subsequent requests for the data only download newly available records plus a few others to ensure continuity.

Currently, only the RRP endpoint is available.

pypi package:

https://pypi.org/project/newyorkfed-pandas/