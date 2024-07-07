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

### App

TODO
