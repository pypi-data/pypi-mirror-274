#! /usr/bin/env python3

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pendulum
import serial
from deprecated import deprecated
from icecream import ic
from loguru import logger
from pydantic import BaseModel
from tqdm import tqdm

from .config import Daq


class RealEvent(BaseModel):
    """実イベント"""

    timestamp: datetime = pendulum.now()
    """測定時刻。宇宙線イベントが通過した日時"""
    top: int = 0
    """topレイヤーのヒット。0 - 10の値"""
    mid: int = 0
    """midレイヤーのヒット。0 - 10の値"""
    btm: int = 0
    """btmレイヤーのヒット。0 - 10の値"""
    adc: int = 0
    """topレイヤーにヒットがあったときのADC値。0 - 1023の値"""
    tmp: float = 0.0
    """BME280で測定した気温。[degC]"""
    atm: float = 0.0
    """BME280で測定した気圧。[Pa]"""
    hmd: float = 0.0
    """BME280で測定した湿度。[%]"""


@deprecated(version="0.6.0", reason="Use typer.Typer for CLIs.")
def init_parser():
    """[deprecated] Initialize argument parser

    :deprecated: `0.6.0`. Replaced with typer.Typer for CLIs.

    """

    now = pendulum.now().strftime("%Y%m%d")

    parser = argparse.ArgumentParser(description="OSECHI DAQ")
    parser.add_argument(
        "--saved",
        default=Path(now),
        type=Path,
        help=f"path to save data. (default={now})",
    )
    parser.add_argument(
        "-q", action="count", default=0, help="decrease verbosity. (default=0)"
    )
    parser.add_argument(
        "--skip", type=int, default=10, help="skip rows to print. (default=10)"
    )

    group1 = parser.add_argument_group("FILE", description="Options for files.")
    group1.add_argument(
        "--prefix",
        default="osechi_data",
        help="set prefix of filename. (default='osechi_data')",
    )
    group1.add_argument(
        "--suffix",
        choices=[".csv", ".dat"],
        default=".csv",
        help="set suffix of filename. (default='.csv')",
    )
    group1.add_argument(
        "--max-rows",
        metavar="ROWS",
        type=int,
        default=10000,
        help="set max. rows per file. (default=10000)",
    )
    group1.add_argument(
        "--max-files",
        metavar="FILES",
        type=int,
        default=100,
        help="set max. files to create. (default=100)",
    )
    group1.add_argument(
        "--append",
        action="store_true",
        help="append data to existing file. (default=False)",
    )

    group2 = parser.add_argument_group(
        "CONNECTION", description="Options for serial connection."
    )
    group2.add_argument(
        "--device",
        default="/dev/ttyUSB0",
        help="set USB device name. (default='/dev/ttyUSB0')",
    )
    group2.add_argument(
        "--baudrate", type=int, default=115200, help="set baudrate. (default=115200)"
    )
    group2.add_argument(
        "--timeout",
        type=int,
        default=1000,
        help="set read timeout in seconds. (default=1000)",
    )

    return parser


def init_saved(daq: Daq) -> None:
    """Initialize destination directory to save data files

    保存先のディレクトリを初期化します。
    ディレクトリが存在しない場合は、作成します。
    ディレクトリが存在する場合は、``FileExistsError``を発行し、終了（``sys.exit``）します。
    ただし。DAQオブジェクトの``--append``オプションが有効な場合は、終了せずに追記を許可します。

    :Args:
    - daq(Daq): DAQ設定オブジェクト

    :Example:

    ```python
    >>> daq = Daq()
    >>> daq.load_toml(load_from)
    ```
    """

    p = Path(daq.saved)
    try:
        p.mkdir()
        msg = f"Created new directory : {p}"
        logger.info(msg)
    except FileExistsError as e:
        msg = f"Directory already exists : {p}"
        logger.warning(msg)
        if not daq.append:
            logger.error(e)
            sys.exit()
        msg = "Overwrite data to existing files."
        logger.warning(msg)

    return


def get_savef(args: Daq, n: int) -> Path:
    """Get filename to save data

    保存するファイル名を生成します。
    DAQ設定の接頭辞（``prefix``）と拡張子（``suffix``）の値を使って
    ``{prefix}_{連番:06}.{suffix}``の形式で生成します。

    :Args:
    - args(Daq): DAQ設定オブジェクト
        - prefix: ファイルの接頭辞
        - suffix: ファイルの拡張子
    - n(int): ファイル番号

    :Example:
    ```console
    osechi_data_000000.csv
    osechi_data_000001.csv
    osechi_data_000002.csv
    ```

    """
    stem = f"{args.prefix}_{n:06}"
    fname = Path(stem).with_suffix(args.suffix)
    savef = Path(args.saved, fname)

    msg = "deprecation warning: use get_savef_with_timestamp instaed."
    logger.warning(msg)

    return savef


def get_savef_with_timestamp(args: Daq, n: int) -> Path:
    """Get filename to save data with timestamp

    作成日を含んだファイル名を生成する。
    ファイル名は、DAQ設定の接頭辞（``prefix``）、ファイルを開いた時刻（``pendulum.now``）と
    拡張子（``suffix``）の値を使って生成する。

    時刻のフォーマットは、ファイル名が分かりやすいように独自フォーマットにした。

    :Args:
        - args (Daq): Daqオブジェクト
        - n (int): ファイル番号

    :Returns:
        - savef (Path): Pathオブジェクト

    :Examples:
    ```console
    20240520/osechi_data_2024-05-20T12h34m56s_000000.csv
    20240520/osechi_data_2024-05-20T13h53m24s_000001.csv
    20240520/osechi_data_2024-05-20T14h46m23s_000000.csv  // 走り直すとリセット
    20240520/osechi_data_2024-05-20T14h36m32s_000001.csv
    ```

    """
    ts = pendulum.now().format("YYYY-MM-DDTHH[h]mm[m]ss[s]")
    stem = f"{args.prefix}_{ts}_{n:06}"
    fname = Path(stem).with_suffix(args.suffix)
    savef = Path(args.saved, fname)
    return savef


@deprecated(version="0.6.0", reason="Use run.")
def daq():
    """[deprecated] Main DAQ

    :deprecated: `0.6.0`. Use `run` instead.


    """
    ic.configureOutput(prefix="[running daq] | ")

    parser = init_parser()
    args = parser.parse_args()
    init_saved(args)

    ic(args)

    # Open serial connection

    with serial.Serial(
        args.device, baudrate=args.baudrate, timeout=args.timeout
    ) as port:
        port.rts = False
        port.dtr = False

        for nfile in tqdm(range(args.max_files), desc="files"):
            savef = get_savef(args, nfile)
            ic(savef)

            with savef.open("a") as f:
                for nrow in tqdm(range(args.max_rows), leave=False, desc="rows"):
                    now = pendulum.now().to_iso8601_string()
                    data = port.readline().decode("utf-8").strip()
                    row = f"{now} {data}"
                    if args.suffix == ".csv":
                        row = (",").join(row.split())
                    f.write(row + "\n")

                    if args.q == 0 and nrow % args.skip == 0:
                        ic(nrow, row)


def open_serial_connection(daq: Daq) -> serial.Serial:
    """Open and return a serial connection.

    シリアル通信（UART）に使うポートを準備します。
    ``with``構文で使う想定です。

    通信に使うUSBポート名（``device``）、
    ボーレート（``baudrate``）、
    通信開始／書き込みのタイムアウト秒（``timeout``）は
    DAQ用の設定ファイルで変更できるようにしてあります。

    :Args:
    - daq(Daq): DAQ設定オブジェクト
        - device: USBポート名
        - baudrate: ボーレート（通信速度）[bps]
        - timeout: タイムアウト秒 [sec]

    :Returns:
    - port(serial.Serial): 通信を開始したシリアルオブジェクト

    :Example:

    ```python
    >>> with open_serial_connection(daq) as port:
    >>>     # データ測定の処理
    >>>
    ```

    """
    port = serial.Serial(
        daq.device,
        baudrate=daq.baudrate,
        timeout=daq.timeout,
        write_timeout=daq.timeout,
    )
    port.rts = False
    port.dtr = False

    # logger.debug(f"Port opened: {port}")

    return port


def write_vth(port: serial.Serial, ch: int, vth: int):
    """Write threshold to OSECHI.

    シリアル通信（UART）を使って閾値を書き込みます。
    値を書き込んだあとに、値が読み出せるかを確認します。

    読み出した値が ``dame`` となっている場合は書き込みに失敗しています。
    その場合は、もういちど設定し直すよう警告を表示します。

    ESP32のバッファサイズの制限から、閾値は2回に分割して転送しています。

    - ``val1`` は vth を右に6ビットシフト（=64で割る）して、head を足した値
    - ``val2`` は vth を左に2ビットシフト（=4をかける）して、下位8ビットを取り出した値

    詳細はこの関数のソースコードを確認してください。
    """
    val = vth
    head = 0b10000
    val1 = head + (val >> 6)
    val2 = (val << 2) & 0xFF

    logger.debug(f"Write: ch = {ch}")
    logger.debug(f"Write: val1 = {val1:b}")
    logger.debug(f"Write: val2 = {val2:b}")

    port.write(ch.to_bytes(1, "big"))
    port.write(val1.to_bytes(1, "big"))
    port.write(val2.to_bytes(1, "big"))

    read0 = port.readline().decode("utf-8", "ignore").strip()
    read1 = port.readline().decode("utf-8", "ignore").strip()
    read2 = port.readline().decode("utf-8", "ignore").strip()

    logger.debug(f"Read: ch = {read0}")
    logger.debug(f"Read: val1 = {read1}")
    logger.debug(f"Read: val2 = {read2}")

    success = False

    if read0 == "dame":
        success = False
        msg = f"Ch{ch}: Set threshold failed. Try again."
        logger.warning(msg)
    elif read0 == str(ch):
        success = True
        msg = f"Ch{ch}: Set threshold to {vth}."
        logger.success(msg)
    else:
        success = True
        msg = f"Ch{ch}: Set threshold to {vth}. Maybe."
        logger.success(msg)
    return success


def set_vth(daq: Daq, ch: int, vth: int) -> bool:
    """Set threshold

    チャンネル番号を指定し、閾値を設定します。
    チャンネル番号は1 - 3 の範囲で指定してください。
    閾値は1 - 1023 の範囲で指定してください。

    書き込みに成功すると ``success=True`` を返します。
    書き込みに失敗した場合は、警告メッセージを表示します。
    このとき、設定済みの閾値はそのままになります。

    :Args:
    - daq(Daq): DAQ設定オブジェクト
    - ch(int): チャンネル番号。1 - 3の範囲で指定してください
    - vth(int): 閾値の値。1 - 1023 の範囲で指定してください
    """

    # check values
    if ch not in range(1, 4):
        msg = f"value of ch is out of range: {ch}"
        logger.error(msg)
        sys.exit()

    if vth not in range(1, 1024):
        msg = f"value of vth is out of range: {vth}"
        logger.error(msg)
        sys.exit()

    init_saved(daq)

    try:
        with open_serial_connection(daq) as port:
            success = write_vth(port, ch, vth)
            fname = Path(daq.saved) / daq.fname_logs

            with fname.open("a", newline="") as f:
                now = pendulum.now().to_iso8601_string()
                row = [str(now), str(ch), str(vth), str(success)]
                writer = csv.writer(f)
                writer.writerow(row)
            msg = f"Saved data to {fname}."
            logger.info(msg)
        return success
    except serial.SerialException as e:
        logger.error(e)
        msg = """Could not open the port. Device name might be wrong.
        Run 'arduino-cli board list' and check the device name.
        Edit 'daq.toml' if you needed.
        """
        logger.warning(msg)
        sys.exit()
    except Exception as e:
        logger.error(e)
        msg = """
        Unaware error occurred.
        Please think if you need to handle this error.
        """
        sys.exit()


def set_vth_retry(daq: Daq, ch: int, vth: int, max_retry: int) -> bool:
    """
    Retry setting threshold.

    :Args:
    - daq (Daq): Daqオブジェクト
    - ch (int): チャンネル番号
    - vth (int): スレッショルド値
    - max_retry (int): 設定に失敗ししたときにトライする最大回数

    :Returns:
    - success (bool): スレッショルド値の設定の結果
    """

    for i in range(max_retry):
        success = set_vth(daq, ch, vth)
        if success:
            return True
        msg = f"Retry: {i} / {max_retry} times."
        logger.warning(msg)

    return False


def read_serial_data(port: serial.Serial) -> list:
    """Read serial data from port.

    OSECHIが接続されているポートからデータを読み出します。
    引数にしていするポートは、あらかじめ開いたものを渡してください。
    ``run_daq``や``time_daq``でデータを取得するために使います。

    :Args:
    - port (serial.Serial): Serialオブジェクト

    :Returns:
    - row (list): 読み出した時刻を追加したデータのリスト

    :Examples:
    ```python
    >>> with open_serial_connection() as port:
    >>>     row = read_serialc_data(port)
    >>>     row
    [日付, top, mid, btm, adc, tmp, atm, hmd]
    ```

    :TODO:
    - list -> RealEventオブジェクトに変換する
    - タイムアウトしたときの処理を整理する

    """
    now = pendulum.now().to_iso8601_string()
    data = port.readline().decode("UTF-8").strip()
    if len(data) == 0:
        msg = f"No data to readout. Timed-out: {port.timeout}"
        logger.warning(msg)
    row = f"{now} {data}".split()
    return row


def save_serial_data(f, daq: Daq, port: serial.Serial) -> list:
    """
    :Args:
    - f: ファイルポインタ
    - daq (Daq): Daqオブジェクト
    - port (serial.Serial): Serialオブジェクト

    :Return:
    - rows (list[list]): 取得したデータのリスト

    :TODO:
    - Daqオブジェクトに依存しない関数にしたい（ジェネレーターにするのがいいのかな？）
    - pd.DataFrameを返した方がいいかもしれない？
    """
    max_rows = daq.max_rows
    rows = []
    for nrow in tqdm(range(max_rows), leave=False, desc="rows"):
        row = read_serial_data(port)
        rows.append(row)
        if daq.suffix == ".csv":
            writer = csv.writer(f)
            writer.writerow(row)
        else:
            writer = csv.writer(f, delimiter=" ")
            writer.writerow(row)
        f.flush()
    return rows


def run_daq(daq: Daq) -> None:
    """メインDAQ

    OSECHIが接続されたUSBポートとシリアル通信をして、データ取得する。
    指定したファイル数と行数をでループ処理する。

    :TODO:
    - 関数名をより適切なものに変えたい
    - while_daq みたいなのを作ってもいいかもしれない
    """
    # Open serial connection
    with open_serial_connection(daq) as port:
        init_saved(daq)

        for nfile in tqdm(range(daq.max_files), desc="files"):
            savef = get_savef_with_timestamp(daq, nfile)
            msg = f"Saving data to: {savef}."
            logger.info(msg)
            logger.info("Press Ctrl-c to stop.")

            with savef.open("a") as f:
                save_serial_data(f, daq, port)

            msg = f"Saved data to: {savef}."
            logger.success(msg)


def run(args: Daq):
    """メインのDAQ

    run_daqのラッパー。例外処理などで囲んだもの。

    :versionadded: `0.6.0`.
    """

    try:
        run_daq(args)
    except serial.SerialException as e:
        logger.error(e)
        msg = """Could not open the port. Device name might be wrong.
        Run 'arduino-cli board list' and check the device name.
        Edit 'daq.toml' if you needed.
        """
        logger.warning(msg)
        sys.exit()
    except KeyboardInterrupt as e:
        logger.warning(e)
        msg = """Quit."""
        logger.info(msg)
        sys.exit()
    except Exception as e:
        logger.error(e)
        msg = """Exit.
        Unaware error occurred.
        Please think if you need to handle this error.
        """
        logger.error(msg)
        sys.exit()


def time_daq(args: Daq, duration: int) -> pd.DataFrame:
    """
    測定時間を指定してDAQを走らせます。

    :Args:
    - args (Daq): Daqオブジェクト
    - duration (int): 測定時間を秒で指定

    :Returns:
    - data (pd.DataFrame): 測定結果のデータフレーム
    """

    rows = []
    with open_serial_connection(args) as port:
        init_saved(args)

        logger.debug("Port opened.")
        daq_start = pendulum.now()
        daq_stop = daq_start.add(seconds=duration)

        logger.debug(f"- DAQ Started: {daq_start}")
        logger.debug(f"- DAQ Stop   : {daq_stop}")

        while pendulum.now() < daq_stop:
            row = read_serial_data(port)
            event = RealEvent()
            event.timestamp = pendulum.parse(row[0])
            event.top = int(row[1])
            event.mid = int(row[2])
            event.btm = int(row[3])
            event.adc = int(row[4])
            event.tmp = float(row[5])
            event.atm = float(row[6])
            event.hmd = float(row[7])
            rows.append(event.model_dump())
    daq_end = pendulum.now()
    diff = daq_end - daq_start
    elapsed_time = diff.in_seconds()
    logger.debug(f"- DAQ Closed : {daq_end} / Elapsed: {elapsed_time} sec.")
    data = pd.DataFrame(rows)
    return data


@deprecated(
    version="0.14.0",
    reason="Will be deprecated. Use threshold.scan_threshold_by_channel instead.",
)
def scan_ch_vth(daq: Daq, duration: int, ch: int, vth: int) -> list:
    """
    Run threshold scan.

    :Args:
    - daq (Daq): Daqオブジェクト
    - duration (int): 測定時間（秒）
    - ch (int): 測定するチャンネル番号
    - vth (int): スレッショルド値

    :Returns:
    - data (list): [測定時刻、チャンネル番号、スレッショルド値、イベント数]のリストを返します。
    """

    logger.warning("Will be deprecated. Please use threshold.scan_by_channel instead.")

    # Try to set the threshold
    if not set_vth_retry(daq, ch, vth, 3):
        msg = f"Failed to set threshold: ch{ch} - {vth}"
        logger.error(msg)
        return []

    # Collect data
    try:
        rows = time_daq(daq, duration)
        counts = len(rows)
        tmp = rows["tmp"].mean()
        atm = rows["atm"].mean()
        hmd = rows["hmd"].mean()
        fname = get_savef_with_timestamp(daq, ch)
        rows.to_csv(fname, index=False)
        msg = f"Saved data to: {fname}"
        logger.info(msg)
    except Exception as e:
        msg = f"Failed to collect data due to: {str(e)}"
        logger.error(msg)
        counts = 0
        tmp = 0
        atm = 0
        hmd = 0

    # Save Summary
    now = pendulum.now().to_iso8601_string()
    data = [now, duration, ch, vth, counts, tmp, atm, hmd]
    fname = Path(daq.saved) / daq.fname_scan
    with fname.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    msg = f"Added data to: {fname}"
    logger.info(msg)

    return data


@deprecated(
    version="0.14.0",
    reason="Will be deprecated. Use threshold.scan_thresholds instead.",
)
def scan_ch_thresholds(
    daq: Daq, duration: int, ch: int, thresholds: list[int]
) -> list[list]:
    """
    Run threshold scan.

    :Args:
    - daq (Daq): Daqオブジェクト
    - duration (int): 測定時間（秒）
    - ch (int): チャンネル番号
    - thresholds (list[int]): スレッショルド値のリスト

    :Returns:
    - rows (list[list]): [測定時刻、チャンネル番号、スレッショルド値、イベント数]のリスト
    """

    logger.warning("Will be deprecated. Please use threshold.scan_thresholds instead.")
    # Estimated time for scan
    msg = f"Number of points: {len(thresholds)}"
    logger.info(msg)
    estimated_time = len(thresholds) * duration
    msg = f"Estimated time: {estimated_time} sec."
    logger.info(msg)

    # すべてのチャンネルの閾値を高くする
    set_vth_retry(daq, 1, 500, 5)
    set_vth_retry(daq, 2, 500, 5)
    set_vth_retry(daq, 3, 500, 5)

    rows = []
    n = len(thresholds)
    for i, vth in enumerate(thresholds):
        msg = "-" * 40 + f"[{i+1:2d}/{n:2d}: {vth}]"
        logger.info(msg)
        row = scan_ch_vth(daq, duration, ch, vth)
        if row:
            rows.append(row)

    return rows


if __name__ == "__main__":
    try:
        daq()
    except KeyboardInterrupt as e:
        ic(e)
        sys.exit()
