# Haniwers : ハニワーズ

墳Qの解析コード（個人用）

![w:300](../docs/_static/haniwer.png)

# ドキュメント

関連するドキュメントは、このリポジトリのGitLab Pagesで公開

- ``haniwers``の使い方（built with sphinx）: https://qumasan.gitlab.io/haniwers/docs/
- 解析ログブック（built with mystmd）: https://qumasan.gitlab.io/haniwers/


---

# できること／したいこと

- [x] 宇宙線検出器OSECHIで取得したデータを、解析可能なCSVファイルに変換する
- [ ] データを理解するのに必要は基本プロットを作成する
- [ ] まとめスライドのテンプレートを作成する


---

# インストール

```console
$ pipx install -i https://test.pypi.org/simple/ haniwers
$ which haniwers
```


---

# 開発者向け

## インストール＆ビルド

- ``haniwers``はDAQツールと解析ツールが同梱されている
- 測定環境と解析環境で作業ディレクトリを分けて、それぞれクローンすることを推奨

### 作業ディレクトリを作成する

```console
// 作業環境を作成する（ディレクトリ名は任意）
$ cd mkdir ~/repos/hnw/

// 測定に使う環境（ディレクトリ）
$ mkdir hnw-daq

// 解析に使う環境（ディレクトリ）
$ mkdir hnw-analysis
```

- 測定環境：タグを指定してリポジトリをクローンする
- 解析環境：最先端のブランチ（``main``）をクローンし、解析トピックごとにブランチを作成する

### 測定に使う環境を構築する

```console
$ cd ~/repos/hnw/hnw-daq/
// タグを指定してクローンする
$ git clone https://gitlab.com/qumasan/haniwers.git -b 0.13.1 --depth 1
$ cd haniwers
$ poetry install
$ poetry shell
(.venv) $ cd sandbox/
(.venv) $ haniwers --help
```

- データ測定環境を構築する場合は、``-b タグ番号``でタグを指定してshallowクローン（``--depth 1``）する
  - 最新のタグ番号は[タグ一覧](https://gitlab.com/qumasan/haniwers/-/tags)で調べる
  - それぞれのタグの内容は[変更履歴（CHANGELOG）](https://gitlab.com/qumasan/haniwers/-/blob/main/CHANGELOG.md)を調べる
- データ測定中に不意にソースコードが更新されないようにする必要がある
  - 測定中にソースコードを更新してしまった場合、どのような動作になるかは分からない
  - 取得したデータの健全性を確保するため、意図しない更新はできるだけ避けるようにする 

### 解析に使う環境を構築する

```console
$ cd ~/repos/hnw/hnw-analysis/
$ git clone https://gitlab.com/qumasan/haniwers.git
$ cd haniwers
$ poetry install
$ poetry shell
(.venv) $ git switch ブランチ名
(.venv) $ cd sandbox/
(.venv) $ haniwers --help
```

---

# 事前準備

## 必要な開発環境

1. [Gitのインストール](https://kumaroot.readthedocs.io/ja/latest/git/git-install.html)
2. [Pythonのインストール](https://kumaroot.readthedocs.io/ja/latest/python/python-install.html)
3. [Poetryのインストール](https://kumaroot.readthedocs.io/ja/latest/python/python-poetry.html)
4. [VS Codeのインストール](https://kumaroot.readthedocs.io/ja/latest/vscode/vscode-install.html)

## Gitの設定

```console
// 現在の設定内容を確認する
$ git config -l

// 基本項目が設定されてない場合
$ git config --global user.name "名前"
$ git config --global user.email "メールアドレス"
$ git config --global pull.rebase false

// エディターを設定したい場合（どれかひとつ）
$ git config --global core.editor emacsclient    # Emacsに設定
$ git config --global core.editor "code --wait"  # VS Codeに設定
$ git config --global core.editor hx             # Helixに設定
```

- Gitをはじめて使う場合、ユーザー名／メールアドレスの基本設定が必要
- 必要であればエディターを設定する（これは後回しでもOK）

## Python環境 /Poetry環境を構築する

```console
$ poetry install
$ poetry shell
(.venv) $ cd sandbox
(.venv) $ haniwers --help
(.venv) $ haniwers version
haniwers 0.12.0
```

---

# ポータブル環境を作成する

Dockerを使ってポータブルな環境（Dockerイメージ）を作成する

## イメージを作成する

```console
$ cd docker
$ docker build --platform=linux/arm64 -t myhaniwers .
```

- Raspberry Piで動作するイメージを作る場合は、``ARM``ベース（``--platform=linux/arm64``）でビルドする
- MacBookなどRPi以外のパソコンでビルドする
  - RPiでイメージをビルドすると、かなり時間がかかる

## イメージを移動する

```console
// MBPで実行する
$ docker save myhaniwers:latest > myhaniwers.tar

// RPiで実行する
$ docker load -i myhaniwers.tar
```

- 作成したイメージを``.tar``形式に出力し、USBメモリにコピーする
- USBメモリから測定用のRPiにイメージをコピーする
- RPiでイメージを読み込む

## コンテナを起動する

```console
$ docker run --rm -it \
    -v $PWD/sandbox:/home/app/haniwers/sandbox \
    --device=/dev/ttyUSB0:/dev/ttyUSB0 \
    myhaniwers:latest bash
```

- ホスト側の``sandbox``をコンテナ側にマウントする
- ホスト側のUSBポート（``/dev/ttyUSB0``）をコンテナ側のUSBポート（``/dev/ttyUSB0``）に接続する
