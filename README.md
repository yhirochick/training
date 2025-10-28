# 数学演習問題PDFジェネレーター

中学校数学の演習問題PDFと解答PDFをDockerとLuaLaTeXで生成するプロジェクトです。

## 特徴

- **対応問題**
  - 中1: 一次方程式
  - 中1: 比例と反比例（x, yの値の組から比例の式を求める）
  - 中2: 連立方程式

- **再現性**: 乱数シードで同一問題セットを再生成可能
- **安定した組版**: LuaLaTeX + Noto CJK フォントで日本語の禁則処理と字間を適切に処理
- **Docker対応**: 環境差異を排除し、どこでも同じPDFを生成

## ディレクトリ構造

```
.
├── Dockerfile                  # Docker環境定義
├── docker-compose.yml          # Docker Compose設定
├── Makefile                    # ビルド自動化
├── README.md                   # このファイル
├── src/
│   ├── generate.py            # メイン生成スクリプト
│   └── generators.py          # 問題生成ロジック
├── templates/
│   ├── problems.tex.j2        # 問題用LaTeXテンプレート
│   └── answers.tex.j2         # 解答用LaTeXテンプレート
└── output/                     # 生成ファイルの出力先
```

## 必要環境

- Docker
- Docker Compose

## 使い方

### 1. Dockerイメージのビルド

初回のみ実行:

```bash
docker compose build
```

### 2. PDFの生成

デフォルトシード（12345）で生成:

```bash
make docker-build
```

カスタムシードで生成:

```bash
make docker-build SEED=54321
```

生成されたPDFは `output/` ディレクトリに配置されます:
- `output/problems.pdf` - 演習問題
- `output/answers.pdf` - 解答

### 3. 生成ファイルのクリーンアップ

```bash
make docker-clean
```

## ローカル環境での実行（Dockerなし）

TeX Live、LuaLaTeX、Python 3、Jinja2がインストールされている場合:

```bash
make build SEED=12345
```

## オプション

### 問題数の変更

`src/generate.py` を直接実行:

```bash
python3 src/generate.py --seed 12345 --num-problems 10
```

その後、LuaLaTeXでコンパイル:

```bash
lualatex -output-directory=output output/problems.tex
lualatex -output-directory=output output/answers.tex
```

## 技術仕様

- **LaTeXエンジン**: LuaLaTeX
- **フォント**: Noto Sans CJK JP
- **テンプレートエンジン**: Jinja2
- **言語**: Python 3
- **コンテナ**: Ubuntu 22.04ベース

## 動作確認

プロジェクトが正しくセットアップされているか確認:

```bash
# クイックテスト（Python環境のみ）
./quick_test.sh

# 再現性の検証
./verify_reproducibility.sh
```

## サンプル出力

シード12345での生成例:

**一次方程式**
- `8x - 20 = -1` → 解: `x = 19/8`
- `3x + 7 = -4` → 解: `x = -11/3`

**比例の式**
```
x | 3  | -3 | -4
y | 27 | -27| -36
```
→ 解: `y = 9x`

**連立方程式**
```
3x + y = 19
4x + y = 27
```
→ 解: `x = 8, y = -5`

## ドキュメント

- `README.md` - このファイル（概要とクイックスタート）
- `DOCKER_GUIDE.md` - Docker環境での詳細な使用方法とトラブルシューティング
- `USAGE.md` - 詳細な使用方法とカスタマイズ
- `PROJECT_STRUCTURE.md` - プロジェクト構成と技術詳細
- `SUMMARY.md` - 実装完了サマリー

## ライセンス

MIT License
