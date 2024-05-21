import sys
from pathlib import Path

import pandas as pd
import pendulum

# from icecream import ic
from loguru import logger


def reformat_datetime(datetime: str) -> str:
    """
    日時を変換する

    Example
    -------

    - ``2022-05-18T20:48:14`` -> ``2022-05-18T20:48:14``
    - ``2022-06-02T18:52:36.442190+09:00`` -> ``2022-06-02T18:52:36``

    """
    dt = pendulum.parse(datetime)
    fmt = dt.format("YYYY-MM-DDTHH:mm:ss")
    return fmt


def load_raw_data(fname: Path, **kwargs) -> pd.DataFrame:
    """
    DAQで取得したデータ形式を ``pd.DataFrame`` に変換して読み込む

    Parameters
    ----------
    fname : Path
        生データのファイル名

    kwargs
        ``pd.read_csv`` の引数を想定

    Returns
    -------
    pd.DataFrame
        データフレーム

    Notes
    -----
    - ファイルの保存形式（＝拡張子）で ``pd.read_csv`` の引数をちょっと変える必要がある。拡張子は ``.dat`` / ``.csv`` だけOKにしてあり、それ以外の場合は ``sys.exit`` する。
    - ``.csv`` はそのままカンマ区切り、``.dat`` はスペース区切り（ ``sep=" "`` ）として、 ``pd.read_csv`` する。
    - ファイル内のカラム名は適当だったり、なかったりする。適切なカラム名を付与する。カラム名はこの関数内にハードコードしている。
    - イベント時刻（ ``time`` ）は ``pd.datetime`` オブジェクトに変換する。使ったDAQのバージョンによって記録された日時の形式が異なるので、それを内部で変換している。
    - 各レイヤーのヒットの有無（ ``True`` / ``False`` ）を確認して、ヒット用のカラム（ ``hit_top`` / ``hit_mid`` / ``hit_btm`` ）に保存する。現在、各レイヤーの値自体には意味がない。そのうち光量など意味を持たせる可能性はあるかも？
    - ヒットのあったレイヤーのパターンを計算して 8ビット で表現する。``hit_type = hit_top * 4 + hit_mid * 2 + hit_btm * 1``
    """

    _names = ["time", "top", "mid", "btm", "adc", "tmp", "atm", "hmd"]
    suffix = fname.suffix
    if suffix == ".dat":
        data = pd.read_csv(fname, names=_names, sep=" ", comment="t", **kwargs)
    elif suffix == ".csv":
        data = pd.read_csv(fname, names=_names, **kwargs)
    else:
        error = f"Unknown suffix : {suffix}"
        logger.error(error)
        sys.exit()

    data["time"] = data["time"].apply(reformat_datetime)
    data["time"] = pd.to_datetime(data["time"], format="ISO8601")
    # 各レイヤーのヒットの有無を確認する
    data["hit_top"] = data["top"] > 0
    data["hit_mid"] = data["mid"] > 0
    data["hit_btm"] = data["btm"] > 0
    # ヒットのあったレイヤーのパターンを8ビットで表現する
    data["hit_type"] = data["hit_top"] * 4 + data["hit_mid"] * 2 + data["hit_btm"] * 1
    return data


def load_files(fnames: list[Path]) -> pd.DataFrame:
    """複数のファイルを読み込み、単一のデータフレームに変換する

    Parameters
    ----------
    fnames : list[Path]
        読み込むファイルの一覧

    Returns
    -------
    pd.DataFrame
        ファイルごとに変換したデータフレームをすべて結合したデータフレーム

    Notes
    -----
    - ``fnames`` で列挙されたファイルごとに、データフレームに変換する
    - ファイル名の一覧が空の場合は終了する
    - 個々のデータフレームを結合して単一のデータフレームを作成する
    - 結合したデータフレームは、時刻（``time``）でソートしておく
    """
    if len(fnames) == 0:
        error = "No files listed"
        logger.error(error)
        sys.exit()

    _loaded = []
    for fname in fnames:
        _data = load_raw_data(fname)
        _loaded.append(_data)
    loaded = pd.concat(_loaded, ignore_index=True)
    loaded = loaded.sort_values(["time"])
    debug = f"Entries : {len(loaded)}"
    logger.debug(debug)
    return loaded
