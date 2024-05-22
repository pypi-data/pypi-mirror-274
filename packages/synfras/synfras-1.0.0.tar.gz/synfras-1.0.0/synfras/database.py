from collections import namedtuple

import pandas as pd
from dynaconf.utils.boxing import DynaBox
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from synfras.config import config


def connect(urls: dict | DynaBox) -> namedtuple:
    return namedtuple('Database', urls.keys())(
        *[create_engine(url) for url in urls.values()]
    )


def query(
    engine: Engine,
    stmt: str,
    params: dict | list[dict] = None,
    fetch: bool = True,
    as_dict: bool = False,
    index_col: str | list[str] | None = None,
) -> None | list[dict] | pd.DataFrame:
    stmt = text(stmt)
    if fetch:
        result = pd.read_sql(
            stmt, engine, params=params, index_col=index_col, coerce_float=True
        )
        if config.get('timezone'):
            _handle_tz(result)
        if as_dict:
            result = result.to_dict(orient='records')
            result = _handle_length(result)
        return result
    else:
        with engine.connect() as conn:
            conn.execute(stmt, params)
            conn.commit()


def _handle_tz(result: pd.DataFrame) -> None:
    for col in result.columns:
        if isinstance(result[col].dtype, pd.DatetimeTZDtype):
            result[col] = result[col].dt.tz_convert(tz=config.timezone)


def _handle_length(result: list[dict]) -> list[dict] | dict:
    if len(result) == 1:
        return result[0]
    elif len(result) == 0:
        return {}
    return result
