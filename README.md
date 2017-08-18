# `tickerplot` package

This package contains all the utility code that can be used by other packages.

TODO : Update this list

## API

The term API is being used very 'loosely' here. Mostly to document what users should expect.

### `nse_utils`

NSE Utils provides following Main APIs

- `nse_get_all_stocks_list` - Returns a generator of all stocks
- `nse_get_name_change_tuples` - Returns a tuple of name changes of the form `(old, new, date)`
- ScripInfoOHLCVD - A named tuple containing the OHLCVD data for a day
- ScripBaseinfoNSE - A named tuple for info about scrip on NSE

### `bse_utils`

- `bse_get_all_stocks_list` - Returns a generator of all stocks
- `ScripBaseinfoBSE` - A named tuple for info about a scrip on BSE


