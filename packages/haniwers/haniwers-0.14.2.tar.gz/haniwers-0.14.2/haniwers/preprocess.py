import sys
from pathlib import Path

import pandas as pd
import polars as pl
from loguru import logger


from .config import RunData


def get_fnames(read_from: str, search_pattern: str) -> list[Path]:
    """
    読み込みたいファイルの一覧を取得します。

    Parameters
    ----------
    read_from : str
        読み込みたいファイルがあるディレクトリを指定します。
    search_pattern : str
        読み込みたいファイルの検索パターンを指定します。

    Returns
    -------
    list[Path]
        読み込みたいファイルをPathオブジェクトに変換した一覧です。
        一覧の中身はファイル名でソートしてあります。
    """
    fnames = sorted(Path(read_from).glob(search_pattern))
    return fnames


def read_data_with_pandas(fnames: list[Path]) -> pd.DataFrame:
    """
    ファイルをpandasで読み込んでpd.DataFrameに変換します。

    Parameters
    ----------
    fnames : list[Path]
        読み込みたいファイルの一覧を指定します。
        get_fnamesで取得したものを想定しています。

    Returns
    -------
    pd.DataFrame
        すべてのファイルを読み込んで結合したデータです。
    """
    names = ["datetime", "top", "mid", "btm", "adc", "tmp", "atm", "hmd"]
    data = []
    for fname in fnames:
        _suffix = fname.suffix
        if _suffix in [".dat"]:
            datum = pd.read_csv(fname, names=names, sep=" ", comment="t")
        elif _suffix in [".csv"]:
            datum = pd.read_csv(fname, names=names)
        else:
            msg = f"Unknown suffix: {_suffix}"
            logger.warning(msg)
            break
        data.append(datum)
    merged = pd.concat(data, ignore_index=True).dropna(how="all")

    if len(merged) == 0:
        msg = "No entries in DataFrame. Exit."
        logger.error(msg)
        sys.exit()

    return merged


def read_data_with_polars(fnames: list[Path]) -> pd.DataFrame:
    """
    ファイルをpolarsで読み込んでpd.DataFrameに変換します。

    Parameters
    ----------
    fnames : list[Path]
        読み込みたいファイルの一覧を指定します。
        get_fnamesで取得したものを想定しています。

    Returns
    -------
    pd.DataFrame
        すべてのファイルを読み込んで結合したデータです。
    """
    names = ["datetime", "top", "mid", "btm", "adc", "tmp", "atm", "hmd"]
    data = []
    for fname in fnames:
        _suffix = fname.suffix
        if _suffix in [".dat"]:
            datum = pl.read_csv(
                fname,
                has_header=False,
                new_columns=names,
                separator=" ",
                comment_char="t",
            )
        elif _suffix in [".csv"]:
            datum = pl.read_csv(fname, has_header=False, new_columns=names)
        else:
            msg = f"Unknown suffix: {_suffix}"
            logger.warning(msg)
            break
        data.append(datum)
    merged = pl.concat(data).to_pandas().dropna(how="all")

    if len(merged) == 0:
        msg = "No entries in DataFrame. Exit."
        logger.error(msg)
        sys.exit()

    return merged


def read_data(fnames: list[Path]) -> pd.DataFrame:
    # data = read_data_with_pandas(fnames)
    data = read_data_with_polars(fnames)
    return data


def add_time(data: pd.DataFrame, offset: int, timezone: str) -> pd.DataFrame:
    data["datetime"] = pd.to_datetime(data["datetime"], format="ISO8601")
    if data["datetime"].dt.tz is None:
        data["datetime"] = data["datetime"].dt.tz_localize(timezone)
    data["datetime_offset"] = pd.to_timedelta(offset, "s")
    data["time"] = data["datetime"] + data["datetime_offset"]
    return data


def add_hit(data: pd.DataFrame) -> pd.DataFrame:
    """
    各シンチのレイヤーにヒット有無の情報を追加します。
    ヒットあり：1
    ヒットなし：0

    Parameters
    ----------
    data : pd.DataFrame
        読み込んだデータを指定します。

    Returns
    -------
    pd.DataFrame
        ヒット情報を追加したデータです。
    """
    copied = data.copy()
    headers = ["top", "mid", "btm"]
    for header in headers:
        name = f"hit_{header}"
        copied[name] = 0
        isT = data[header] > 0
        copied.loc[isT, name] = 1
    return copied


def add_hit_type(data: pd.DataFrame) -> pd.DataFrame:
    """
    各シンチのヒット情報から、ヒットの種類を計算します。
    ヒット情報が計算できてない場合は、警告を表示し、元のデータを返します。

    Parameters
    ----------
    data : pd.DataFrame
        ヒット情報が入ったデータを指定します。

    Returns
    -------
    pd.DataFrame
        ヒットの種類を追加したデータです。
    """
    _header = "hit_top"
    if _header not in data.columns:
        msg = f"Header '{_header}' does not exist in current dataframe."
        logger.warning(msg)
        return data
    data["hit_type"] = 4 * data["hit_top"] + 2 * data["hit_mid"] + data["hit_btm"]
    return data


def resample_data(data: pd.DataFrame, interval: int):
    """時間を指定して測定データを再集計する

    ``data``に指定した測定データを``pandas.DataFrame.resample``で再集計します。
    データは前処理済みのデータを指定してください。
    再集計したデータをさらに、再集計することもできます。

    - 入力データに必要なカラム: ``["time", "hit_type", "hit_top", "hit_mid", "hit_btm", "adc", "tmp", "atm", "hmd"]
    - 出力データに追加されるカラム: ``["interval", "event_rate", "event_rate_top", "event_rate_mid", "event_rate_btm"]

    :Args:
        - data (pd.DataFrame): 読み込んだデータを指定。
        - interval (int): 再集計する時間間隔（秒）を指定

    :Returns:
        - merged (pd.DataFrame): 指定した時間間隔で再集計したデータ
    """

    # 再集計する時間間隔
    rule = f"{interval}s"

    # 元データのコピーを作成
    copied = data.copy()
    # インデックスを datetime オブジェクトに変更
    copied.index = copied["time"]

    # count
    headers = {"hit_type": "events"}
    keys = list(headers.keys())
    _count = copied.resample(rule)[keys].count().reset_index().rename(columns=headers)

    # sum: 合計値
    headers = {
        "hit_top": "hit_top_sum",
        "hit_mid": "hit_mid_sum",
        "hit_btm": "hit_btm_sum",
    }
    keys = list(headers.keys())
    _sum = copied.resample(rule)[keys].sum().reset_index()

    # mean: 平均値
    headers = {
        "adc": "adc_mean",
        "tmp": "tmp_mean",
        "atm": "atm_mean",
        "hmd": "hmd_mean",
    }
    keys = list(headers.keys())
    _mean = copied.resample(rule)[keys].mean().reset_index()

    # std : 標準偏差
    headers = {
        "adc": "adc_std",
        "tmp": "tmp_std",
        "atm": "atm_std",
        "hmd": "hmd_std",
    }
    keys = list(headers.keys())
    _std = copied.resample(rule)[keys].std().reset_index().rename(columns=headers)

    # 測定日時（time）で結合
    m1 = pd.merge(_count, _sum, on="time")
    m2 = pd.merge(m1, _mean, on="time")
    merged = pd.merge(m2, _std, on="time")

    # レートを計算
    merged["interval"] = interval
    merged["event_rate"] = merged["events"] / merged["interval"]
    merged["event_rate_top"] = merged["hit_top"] / merged["interval"]
    merged["event_rate_mid"] = merged["hit_mid"] / merged["interval"]
    merged["event_rate_btm"] = merged["hit_btm"] / merged["interval"]

    # 測定時間を計算
    epoch = merged["time"].min()
    merged["days"] = merged["time"] - epoch
    merged["seconds"] = merged["days"].dt.total_seconds()

    return merged


def resample_data_loop(data: pd.DataFrame, interval: int) -> pd.DataFrame:
    """
    ヒット種類ごとに時間で再集計します。

    Parameters
    ----------
    data : pd.DataFrame
        ヒットの種類を追加したデータを指定します。
    rule: str
        再集計する時間の頻度を指定します。

    Returns
    -------
    pd.DataFrame
        ヒットの種類ごとに時間で再集計したデータです。
    """
    hit_types = sorted(data["hit_type"].unique())
    rdata = []
    for ht in hit_types:
        q = f"hit_type == {ht}"
        qdata = data.query(q).copy()
        _resampled = resample_data(qdata, interval)
        _resampled["hit_type"] = ht
        rdata.append(_resampled)

    resampled = pd.concat(rdata, ignore_index=True)
    resampled = resampled.sort_values(["time", "hit_type"])
    return resampled


def preprocess_data(
    data: pd.DataFrame, interval: int, datetime_offset: int, timezone: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = add_time(data, offset=datetime_offset, timezone=timezone)
    data = add_hit(data)
    data = add_hit_type(data)
    resampled = resample_data_loop(data, interval)
    return data, resampled


def raw2csv(
    fnames: list[Path], interval: int, datetime_offset: int, timezone: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if len(fnames) == 0:
        msg = "No files found."
        logger.error(msg)
        sys.exit()
    data = read_data(fnames)
    data, resampled = preprocess_data(data, interval, datetime_offset, timezone)
    return data, resampled


def run2csv(run: RunData) -> tuple[pd.DataFrame, pd.DataFrame]:
    fnames = get_fnames(read_from=run.read_from, search_pattern=run.srcf)
    interval = run.interval
    datetime_offset = run.datetime_offset
    timezone = "UTC+09:00"

    data, resampled = raw2csv(fnames, interval, datetime_offset, timezone)
    data["runid"] = run.run_id
    data["name"] = run.name
    data["description"] = run.description

    resampled["runid"] = run.run_id
    resampled["name"] = run.name
    resampled["description"] = run.description

    return data, resampled


if __name__ == "__main__":
    fname = "../data/raw_data/20230806_run17/osechi_data_000000.csv"
    fnames = [Path(fname)]
    gzip, csv = raw2csv(fnames, interval=600, datetime_offset=0, timezone="UTC+09:00")
    logger.debug(f"raw2gz  = {len(gzip)}")
    logger.debug(f"raw2csv = {len(csv)}")
