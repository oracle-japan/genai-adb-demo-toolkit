# genai-adb-demo-toolkit

## これはなに？

OCI Generative AI Service と Autonomous Database を用いて、RAG 構成のデモを行うためのリポジトリです。
OCI Generative AI Service, Autonomous Database に関する操作は、LangChain にて提供されている機能を用いて実装されています。

## 使い方

### 前提事項

- Python 3.11+が実行できる環境であること
- Public Subnet 上に配置された Autonomous Database が作成済みであること

### Notebook

（任意）Python の仮想環境を作成します。

```sh
cd notebook
python3 -m venv .venv
```

仮想環境を有効化します。

```sh
source .venv/bin/activate
```

Notebook 内で使用する依存ライブラリをダウンロードします。

```sh
pip install -r requirements.txt
```

[01_setup-oraclevs.ipynb](./notebook/01_setup-oraclevs.ipynb) を順番に実行します。

### App

[01_setup-oraclevs.ipynb](./notebook/01_setup-oraclevs.ipynb) が実施済みなことが前提となっています。

アプリケーションを起動します。

```sh
streamlit run main.py
```

アプリケーションが、[http://localhost:8501](http://localhost:8501) で起動するので、ブラウザからアクセスします。

#### 現状サポートしているパラメータについて

アプリケーションのサイドバーでは、モデルのパラメータや Vector Search の必要有無などいくつかのパラメータを変更することができます。変更可能なパラメータの簡単な説明は以下の通りです。

| パラメータ        | 概要                                                                                                                 | 設定可能な値                                      |
| ----------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Use Vector Search | Autonomous Database に格納されているデータを LLM の回答生成に含めるかどうか？                                        | `True` or `False`                                 |
| Fetch k           | Vector Search による類似検索で上位何件の結果を取得するか？                                                           | 1~20(アプリの設定で変更可能)                      |
| Model Name        | 使用するモデル                                                                                                       | `cohere.command-r-plus` or `cohere.command-r-16k` |
| Streaming         | LLM によって生成されたチャンクを生成されるたびにクライアントに送るか否か？                                           | `True` or `False`                                 |
| Max Tokens        | LLM が生成する回答の最大長                                                                                           | 10~1024                                           |
| Temperature       | LLM が生成する回答にどの程度ランダム性を持たせるか？（0: 決定論的、1: ランダムサンプリング）                         | 0~1                                               |
| Top k             | LLM が生成するトークンを確率上位何件から取得するのか？（0 を指定した場合は、このサンプリングを使用しないことを示す） | 0~500                                             |
| Top p             | LLM が生成するトークンを確率上位何%をサンプリング対象に加えるか？                                                    | 0~1                                               |
| Frequency Penalty | トークンが頻繁に表示される場合に割り当てられるペナルティのこと                                                       | 0~1                                               |
| Presence Penalty  | 出力に表示された各トークンに割り当てられ、使用されていないトークンを使用した出力の生成を促すペナルティのこと         | 0~1                                               |
