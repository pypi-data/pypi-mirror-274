#! /usr/bin/env python3

from pathlib import Path
from typing import Dict, List

import pandas as pd
from deprecated import deprecated
from loguru import logger

from .config import RunData
from .dataset import load_files


@deprecated(version="0.3.0", reason="Use preprocess.resample_data.")
def resample_data(data: pd.DataFrame, interval: int) -> pd.DataFrame:
    """データフレームをリサンプリングする

    ``time`` をキーにして ``interval`` 間隔でリサンプリングして集計する。
    集計する内容は下記の通り。

    #. ``size`` : サンプリング数（＝ヒット数）
    #. ``sum`` : 上段 / 中段 / 下段 の合計値
    #. ``cumsum`` : 上段 / 中段 / 下段 の累積和
    #. ``mean`` : 平均値
    #. ``std`` : （不偏）標準偏差
    #. ``var`` : （不偏）分散

    Returns
    -------
    pd.DataFrame
        ``time`` をキーにして結合したデータフレーム
    """

    # インデックスを time に変更
    data.index = data["time"]

    # サンプリング間隔（秒数で指定）
    freq = f"{interval}s"

    # サンプリング数を求める
    renames: Dict[int, str] = {0: "hit"}  # type: ignore
    # fmt: off
    _size = (
        data.resample(freq)
        .size()
        .reset_index().rename(columns=renames)
    )
    # fmt: on

    # 合計を求める
    names = [
        "adc",
        "hit_top",
        "hit_mid",
        "hit_btm",
    ]
    # fmt: off
    _sum = (
        data.resample(freq)[names]
        .sum()
        .reset_index()
    )
    # fmt: on

    # 平均値を求める
    names = [
        "adc",
        "hit_top",
        "hit_mid",
        "hit_btm",
        "tmp",
        "atm",
        "hmd",
    ]
    renames: Dict[str, str] = {  # type: ignore
        "adc": "adc_mean",
        "tmp": "tmp_mean",
        "atm": "atm_mean",
        "hmd": "hmd_mean",
        "hit_top": "hit_top_mean",
        "hit_mid": "hit_mid_mean",
        "hit_btm": "hit_btm_mean",
    }
    # fmt: off
    _mean = (
        data.resample(freq)[names]
        .mean()
        .reset_index().rename(columns=renames)
    )
    # fmt: on

    # 標準偏差を求める
    renames: Dict[str, str] = {  # type: ignore
        "adc": "adc_std",
        "tmp": "tmp_std",
        "atm": "atm_std",
        "hmd": "hmd_std",
        "hit_top": "hit_top_std",
        "hit_mid": "hit_mid_std",
        "hit_btm": "hit_btm_std",
    }
    # fmt: off
    _std = (
        data.resample(freq)[names]
        .std()
        .reset_index().rename(columns=renames)
    )
    # fmt: on

    # データフレームをまとめる
    # fmt: off
    resampled = (
        _size
        .merge(_sum, on="time")
        .merge(_mean, on="time")
        .merge(_std, on="time")
    )
    # fmt: on

    # 累積和を求める
    resampled["hit_top_sum"] = resampled["hit_top"].cumsum()
    resampled["hit_mid_sum"] = resampled["hit_mid"].cumsum()
    resampled["hit_btm_sum"] = resampled["hit_btm"].cumsum()
    resampled["adc_sum"] = resampled["adc"].cumsum()
    resampled["hit_sum"] = resampled["hit"].cumsum()

    # ヒットレートを計算する
    resampled["interval"] = interval
    resampled["hit_rate"] = resampled["hit"] / interval
    resampled["hit_top_rate"] = resampled["hit_top"] / interval
    resampled["hit_mid_rate"] = resampled["hit_mid"] / interval
    resampled["hit_btm_rate"] = resampled["hit_btm"] / interval

    # 測定時間を計算する
    epoch = resampled["time"].min()
    resampled["days"] = resampled["time"] - epoch
    resampled["seconds"] = resampled["days"].dt.total_seconds()

    return resampled


@deprecated(version="0.3.0", reason="Use preprocess.preprocess_data.")
def parse_data(data: pd.DataFrame, rules: dict, interval: int) -> pd.DataFrame:
    """
    データフレームを整理する

    1. イベントカテゴリの数だけデータフレームを分割する
    2. サンプリング間隔が設定されている場合はサンプリング集計する
    3. 分割したデータフレームを1つに統合する

    Parameters
    ----------
    data : pd.DataFrame
        入力データ
    rules : dict
        イベントカテゴリ
    interval : int
        サンプリング間隔（秒）

    Returns
    -------
    pd.DataFrame
        整理したデータ
    """
    _parsed = []
    for name, rule in rules.items():
        _sliced = data.query(rule).copy()
        _sliced = resample_data(_sliced, interval)
        _sliced["hit_type"] = name
        _sliced["condition"] = rule
        _parsed.append(_sliced)

    # 1つのデータフレームにまとめる
    # 時刻（time）とイベントタイプ（hit_type）でソートする
    parsed = pd.concat(_parsed, ignore_index=True)
    parsed = parsed.sort_values(by=["time", "hit_type"])
    return parsed


@deprecated(version="0.3.0", reason="Use preprocess.raw2csv.")
def parse_files(
    fnames: List[Path], rules: Dict[str, str], interval: int
) -> pd.DataFrame:
    loaded = load_files(fnames)
    parsed = parse_data(loaded, rules, interval)
    return parsed


@deprecated(version="0.3.0", reason="Use preprocess.run2csv.")
def parser(data: RunData, rules: dict) -> pd.DataFrame:
    fnames = data.fnames

    # Load rawdata and save as raw2gz
    savef = data.raw2gz
    loaded = load_files(fnames)
    loaded["runid"] = data.runid
    loaded["name"] = data.name

    if savef:
        loaded.to_csv(savef, index=False, compression="gzip")
        info = f"Saved as {savef}"
        logger.success(info)

    # Parse rawdata and save as raw2csv
    savef = data.raw2csv
    parsed = parse_data(loaded, rules=rules, interval=data.interval)
    parsed["runid"] = data.runid
    parsed["name"] = data.name
    parsed["desc"] = data.description

    if savef:
        parsed.to_csv(savef, index=False)
        info = f"Saved as {savef}"
        logger.success(info)
