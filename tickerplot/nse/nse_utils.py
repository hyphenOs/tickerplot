#
# Refer to LICENSE file and README file for licensing information.
#
"""
Common utilities for getting stocks, indices data from NSE.
"""
from __future__ import print_function

import os
from collections import namedtuple
import logging


import requests


_logger = logging.getLogger(__name__)

ScripOHLCVD = namedtuple('ScripOHLCVD',
                            ['open', 'high', 'low', 'close', 'volume', 'deliv'])

ScripBaseinfoNSE = namedtuple('ScripBaseinfoNSE',
                                    ['symbol', 'name', 'listing_date', 'isin'])

_ALL_STOCKS_CSV_URL = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'

#_NAME_CHANGE_CSV_URL = 'https://archives.nseindia.com/content/equities/namechange.csv'
_SYM_CHANGE_CSV_URL = 'https://archives.nseindia.com/content/equities/symbolchange.csv'

def nse_get_all_stocks_list(start=None, count=-1):
    """ Returns a generator object of all stocks as a
        namedtuple(symbol, name, listing_date, isin)"""

    start = start or 0
    try:
        start = int(start) or 0
        count = int(count) or -1
    except ValueError: # Make sure both start and count can be 'int'ed
        raise

    r = requests.get(_ALL_STOCKS_CSV_URL)
    module_logger.info("GET: %s", _ALL_STOCKS_CSV_URL)
    if r.ok:
        i = 0
        for line in r.text.split("\n"):
            line = line.split(",")
            if len(line) < 8:
                module_logger.info("Unhandled line: %s", line)
                continue
            symbol = line[0].strip('"')
            if symbol.lower().strip() == 'symbol':
                continue
            if i < start:
                i += 1
                continue
            if count > 0 and i >= start+count:
                raise StopIteration
            name = line[2].strip('"')
            listing_date = line[3].strip('"')
            isin = line[1].strip('"')
            a = ScripBaseinfoNSE(symbol, name, listing_date, isin)
            module_logger.debug("ScripBaseInfoNSE: %s", str(a))
            i += 1
            yield a
    else:
        _logger.error("GET: %s(%d)", ALL_STOCKS_CSV_URL, r.status_code)
        raise StopIteration

def nse_get_sym_change_tuples():
    """Returns a list of name changes as a tuples, the most current name
    is the last name in the tuple."""

    r = requests.get(_SYM_CHANGE_CSV_URL)
    if not r.ok:
        return []

    name_tuples = []
    for line in r.text.split('\n'):
        x = line.split(',')
        if len(x) < 3:
            continue
        name, prev, cur, chdate = x[0].strip(), x[1].strip(), x[2].strip(), x[3].strip()
        if chdate == 'SM_APPLICABLE_FROM': # First line
            continue
        name_tuples.append((prev, cur, chdate,))

    return name_tuples

if __name__ == '__main__':
    nse_get_name_change_tuples()
    for stocks in nse_get_all_stocks_list(count=-1):
        print (stocks)
