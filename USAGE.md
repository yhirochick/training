# 使用方法詳細

## クイックスタート

### Docker環境で実行（推奨）

```bash
# 1. Dockerイメージをビルド
docker compose build

# 2. PDFを生成（デフォルトシード: 12345）
make docker-build

# 3. 生成されたPDFを確認
ls output/
# problems.pdf  - 問題用PDF
# answers.pdf   - 解答用PDF
```

### カスタムシードでの生成

同じシード値を使えば、常に同じ問題セットを生成できます。

```bash
# シード12345で生成
make docker-build SEED=12345

# シード54321で生成
make docker-build SEED=54321
```

## 詳細オプション

### 問題数をカスタマイズ

各セクション（一次方程式、比例、連立方程式）の問題数を変更:

```bash
# Dockerコンテナに入る
docker compose run --rm latex-builder bash

# コンテナ内で実行（例: 各セクション10問）
python3 src/generate.py --seed 12345 --num-problems 10

# PDFをコンパイル
lualatex -output-directory=output output/problems.tex
lualatex -output-directory=output output/problems.tex  # 目次や参照のため2回実行
lualatex -output-directory=output output/answers.tex
lualatex -output-directory=output output/answers.tex

exit
```

### 生成されるファイル

```
output/
├── problems.tex      # 問題用LaTeXソース
├── problems.pdf      # 問題用PDF
├── answers.tex       # 解答用LaTeXソース
├── answers.pdf       # 解答用PDF
└── *.aux, *.log      # LaTeXの補助ファイル
```

## 問題の種類

### 1. 中1: 一次方程式

形式: `ax + b = c` または `ax - b = c`

例:
- `8x - 20 = -1` → 解: `x = 19/8`
- `3x + 7 = -4` → 解: `x = -11/3`

### 2. 中1: 比例の式を求める

x と y の値の組から比例定数を求め、比例の式 `y = ax` を導出

例:
```
x | 3  | -3 | -4
y | 27 | -27| -36
```
→ 解: `y = 9x`

### 3. 中2: 連立方程式

2つの一次方程式からなる連立方程式を解く

例:
```
3x + y = 19
4x + y = 27
```
→ 解: `x = 8, y = -5`

## トラブルシューティング

### Dockerの権限エラー

```bash
# ユーザーをdockerグループに追加（Linuxの場合）
sudo usermod -aG docker $USER
# 再ログイン後に反映
```

### フォントが見つからないエラー

Dockerイメージを再ビルドしてください:

```bash
docker compose build --no-cache
```

### PDFが生成されない

1. TeXファイルが正しく生成されているか確認:
   ```bash
   ls output/*.tex
   ```

2. LuaLaTeXのエラーログを確認:
   ```bash
   cat output/problems.log
   ```

## ローカル環境での実行（Dockerなし）

### 必要なパッケージ（Ubuntu/Debian）

```bash
sudo apt-get update
sudo apt-get install -y texlive-full texlive-luatex texlive-lang-japanese \
                        fonts-noto-cjk python3 python3-pip make
pip3 install jinja2
```

### 実行

```bash
make build SEED=12345
```

## カスタマイズ

### 問題生成ロジックの変更

`src/generators.py` の各クラスを編集:

- `LinearEquationGenerator`: 一次方程式
- `ProportionalFunctionGenerator`: 比例
- `SimultaneousEquationGenerator`: 連立方程式

### LaTeXテンプレートの変更

`templates/` ディレクトリのJinja2テンプレートを編集:

- `problems.tex.j2`: 問題用
- `answers.tex.j2`: 解答用

変更後、再生成:

```bash
python3 src/generate.py --seed 12345
```

## 再現性の確認

同じシードで複数回生成し、TeXファイルが一致することを確認:

```bash
# 1回目
python3 src/generate.py --seed 12345
cp output/problems.tex output/problems_1.tex

# 2回目
python3 src/generate.py --seed 12345
cp output/problems.tex output/problems_2.tex

# 差分確認（何も出力されなければ同一）
diff output/problems_1.tex output/problems_2.tex
```
