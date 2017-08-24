"""
A wrapper script that hides all the details behind SQLAlchemy Core.
"""

import datetime

from sqlalchemy import Table, Column, UniqueConstraint
from sqlalchemy import Integer, String, Float, Date, Boolean, Enum, BigInteger
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from sqlalchemy.sql import select as select_expr_
select_expr = select_expr_

from sqlalchemy import and_
and_expr = and_

from tickerplot.bse.bse_utils import BSEGroup

import enum
class CorpActionEnum(enum.Enum):
    D = 'D'
    B = 'B'
    S = 'S'

class TickerplotExceptionNoMetadata(Exception):
    pass

class TickerplotExceptionNoDBEngine(Exception):
    pass

def create_or_get_all_scrips_table(metadata=None):
    """
    Creates All Scrips Info Table.

    Following information is saved about all scripts that are traded on NSE
    and BSE.

    security_isin : Unique for every security. Used as primary key.
    company_name : Name of the company.
    nse_traded : Flag indicating whether this security is traded on NSE.
    nse_symbol : Symbol on NSE
    nse_start_date : Start date for NSE.
    nse_suspended : Flag indicating whether suspended on NSE
    bse_traded : Flag indicating whether the script is traded on BSE.
    bse_start_date : Start date on BSE.
    bse_id : BSE ID for the script.
    bse_group: BSE Group for the script.
    """
    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    table_name = 'all_scrips_info'
    if table_name not in meta_data.tables :
        all_scrips_tbl = Table(table_name, meta_data,
                Column('security_isin', String(16), primary_key=True),
                Column('company_name', String(80)),
                Column('nse_traded', Boolean, default=False),
                Column('nse_start_date', Date,
                            default=datetime.date(year=2001, day=1, month=1)),
                Column('nse_symbol', String(20)),
                Column('nse_suspended', Boolean, default=False),
                Column('bse_traded', Boolean, default=False),
                Column('bse_start_date', Date,
                            default=datetime.date(year=2001, day=1, month=1)),
                Column('bse_id', String(6)),
                Column('bse_symbol', String(20)),
                Column('bse_group', Enum(BSEGroup)),
                )
        all_scrips_tbl.create(checkfirst=True)
    else:
        all_scrips_tbl = meta_data.tables[table_name]

    return all_scrips_tbl

def create_or_get_nse_bhav_deliv_download_info(metadata=None):
    """
    Creates a table indicating whether NSE Bhavcopy/Deliver data is downloaded.

    date: date for which data is downloaded
    bhav_success: boolean indicating whether data is downloaded for bhavcopy
    deliv_success: boolean indicating whether data is downloaded for delivery
    error_type : Number of times error occurred
    """

    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    table_name = 'nse_bhav_deliv_download_info'
    if table_name not in meta_data.tables :
        nse_bhav_deliv_dl_info = Table(table_name, meta_data,
                    Column('download_date', Date, unique=True),
                    Column('bhav_success', Boolean, default=False),
                    Column('deliv_success', Boolean, default=False),
                    Column('error_type', String(16), default="DLOAD_ERR"),
                    )
        nse_bhav_deliv_dl_info.create(checkfirst=True)
    else:
        nse_bhav_deliv_dl_info = meta_data.tables[table_name]

    return nse_bhav_deliv_dl_info

def create_or_get_nse_equities_hist_data(metadata=None):
    """
    Creates a table of NSE Equities Historical Data.

    Since we download NSE historical data as a bhavcopy, we are storing this
    data in a DB because we are downloading using bhavcopy files and we need
    to have this in the stock:ohlcvd format.

    symbol : Symbol for the security traded.
    date : Date of the security traded.
    open : Open price
    high : High price
    low  : Low price
    close: Close price.
    volume: Total traded volume
    delivery : Total delivery for the security for the day.
    """

    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    table_name = 'nse_equities_hist_data'
    if table_name not in meta_data.tables:
        nse_eq_hist_data = Table(table_name, meta_data,
                            Column('symbol', String(64)),
                            Column('date', Date),
                            Column('open', Float),
                            Column('high', Float),
                            Column('low', Float),
                            Column('close', Float),
                            Column('volume', BigInteger),
                            Column('delivery', BigInteger),
                            UniqueConstraint('symbol', 'date', name='symbol_date'),
                            )
        nse_eq_hist_data.create(checkfirst=True)
    else:
        nse_eq_hist_data = meta_data.tables[table_name]

    return nse_eq_hist_data

def create_or_get_nse_indices_hist_data(metadata=None):
    """
    Creates table for NSE Indices Historical data.

    Each row is of the form -

    symbol : Index symbol (our internal symbol)
    date : Date for the values
    open : open value
    high : high valu
    low : low value
    close : close value.

    We don't need other data like volume/delivery.
    """

    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    table_name = 'nse_indices_hist_data'
    if table_name not in meta_data.tables:
        nse_idx_hist_data = Table(table_name, meta_data,
                            Column('symbol', String(64)),
                            Column('date', Date),
                            Column('open', Float),
                            Column('high', Float),
                            Column('low', Float),
                            Column('close', Float),
                            UniqueConstraint('symbol', 'date', name='symbol_date'),
                            )
        nse_idx_hist_data.create(checkfirst=True)
    else:
        nse_idx_hist_data = meta_data.tables[table_name]

    return nse_idx_hist_data

def create_or_get_nse_corp_actions_hist_data(metadata=None):
    """
    Creates table for NSE Corporate Actions data.

    symbol : NSE symbol for the stock.
    ex_date : Ex Date for the Corporate Action
    action : One of B/S/D (Bonus/Split/Dividend)
    ratio : Multiplier to be applied to preceeding data.
    delta : For dividend difference to be applied to stock price.
    """

    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    table_name = 'nse_corp_actions_hist_data'
    if table_name not in meta_data.tables:
        nse_ca_hist_data = Table(table_name, meta_data,
                                Column('symbol', String(64)),
                                Column('ex_date', Date),
                                Column('action', Enum(CorpActionEnum)),
                                Column('ratio', Float),
                                Column('delta', Float),
                                UniqueConstraint('symbol', 'ex_date', 'action'),
                                )
        nse_ca_hist_data.create(checkfirst=True)
    else:
        nse_ca_hist_data = meta_data.tables[table_name]

    return nse_ca_hist_data

def get_metadata(db_str=None):

    if not db_str:
        return None

    return MetaData(bind=db_str)

def get_engine(metadata=None):

    if not metadata:
        raise TickerplotExceptionNoMetadata

    meta_data = metadata

    return meta_data.bind

def execute_one_insert(statement, ignore_error=True, engine=None):
    result = None
    try:
        result = _do_execute_one(statement, engine)
    except IntegrityError:
        if ignore_error:
            pass
        raise
    return result

def execute_many_insert(statements, ignore_error=True, engine=None):
    results = []
    for statement in statements:
        try:
            result = _do_execute_one(statement, engine)
            results.append(result)
        except IntegrityError:
            if ignore_error:
                continue
            raise
    return results

def execute_one(statement, engine=None):
    return _do_execute_one(statement, engine)

def _do_execute_one(statement, engine=None):

    if not engine:
        raise TickerplotExceptionNoDBEngine

    result = engine.execute(statement)

    return result

if __name__ == '__main__':
    print(create_or_get_all_scrips_table())

