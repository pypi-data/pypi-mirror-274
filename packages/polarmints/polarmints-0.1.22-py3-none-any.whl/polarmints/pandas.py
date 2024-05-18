from __future__ import annotations
import logging
from tempfile import NamedTemporaryFile
import numpy as np
import pandas as pd
from typing import Dict
from functools import partial
from swarkn.helpers import swallow_exception

DFPd = pd.DataFrame
logger = logging.getLogger(__name__)

def dfat(df: DFPd, index, col, default=None):
    """

    similar to df.at[idx, col] but returns None instead of throwing
    """
    try:
        res = df.at[index, col]
        if pd.isnull(res):
            return default
        return res
    except (ValueError, KeyError):
        return default


def get_duplicates(primary_key: list, df: DFPd,
                   report_cols: str | list
                   ) -> DFPd:
    """
    groups duplicates by primary key (PK) displaying all additional report_cols
    """
    dup = df[df[pk].duplicated(keep=False)]
    grouped = dup.groupby(pk)[report_cols].apply(set)
    return grouped

def hconcat_exc(df1: DFPd, df2: DFPd) -> DFPd:
    cols = [c for c in df2.columns if c not in df1.columns]
    res = df1.join(df2[cols])
    return res

def get_at_level(df: DFPd, level: int, key: str) -> DFPd:
    return df.loc[:,
        df.columns.get_level_values(level) == key
    ].droplevel(level, axis=1)

def compare(df1: DFPd, df2: DFPd, **kwargs) -> Tuple[DFPd, dict]:
    a_not_b = df1.index.difference(df2.index).sort_values()
    b_not_a = df2.index.difference(df1.index).sort_values()

    cols = df1.columns.intersection((df2.columns))
    df1f = df1.loc[df1.index.isin(df2.index), cols].sort_index()
    df2f = df2.loc[df2.index.isin(df1.index), cols].sort_index()
    diff = df1f.compare(df2f, **kwargs)
    diffcols = diff.columns.get_level_values(0).unique()
    return diff, dict(
        diff=diff,
        df1=df1f.loc[diff.index, diffcols],
        df2=df2f.loc[diff.index, diffcols],
        df1only=df1.loc[a_not_b, :],
        df2only=df2.loc[b_not_a, :],
        df1str='\n'.join(a_not_b.astype(str)),
        df2str='\n'.join(b_not_a.astype(str)),
    )

def dict2xl(dfs: Dict[DFPd], path: str = None, **kwargs):
    path = path or f'{NamedTemporaryFile().name}.xlsx'
    writer = pd.ExcelWriter(path)
    logger.info(f"writing xlsx to {path}")
    for sheet, df in dfs.items():
        with swallow_exception():
            df.to_excel(writer, sheet_name=sheet, **kwargs)
    writer.close()
