# プロジェクト構成

## ディレクトリツリー

```
training/
├── Dockerfile                      # Docker環境定義
├── docker-compose.yml              # Docker Compose設定
├── Makefile                        # ビルド自動化
├── README.md                       # プロジェクト概要
├── USAGE.md                        # 詳細な使用方法
├── PROJECT_STRUCTURE.md            # このファイル
├── verify_reproducibility.sh      # 再現性検証スクリプト
├── .gitignore                      # Git除外設定
│
├── src/                            # Pythonソースコード
│   ├── generate.py                 # メイン生成スクリプト
│   └── generators.py               # 問題生成ロジック
│
├── templates/                      # LaTeXテンプレート（Jinja2）
│   ├── problems.tex.j2             # 問題用テンプレート
│   └── answers.tex.j2              # 解答用テンプレート
│
└── output/                         # 生成ファイル出力先（gitignore）
    ├── problems.tex                # 生成された問題用LaTeX
    ├── problems.pdf                # 問題用PDF
    ├── answers.tex                 # 生成された解答用LaTeX
    └── answers.pdf                 # 解答用PDF
```

## ファイル説明

### ルートディレクトリ

| ファイル | 説明 |
|---------|------|
| `Dockerfile` | Ubuntu 22.04ベースのLuaLaTeX環境を構築 |
| `docker-compose.yml` | Dockerサービス定義、ボリュームマウント設定 |
| `Makefile` | `make docker-build`などのビルドコマンド定義 |
| `README.md` | プロジェクト概要、クイックスタートガイド |
| `USAGE.md` | 詳細な使用方法、カスタマイズ、トラブルシューティング |
| `PROJECT_STRUCTURE.md` | このファイル、プロジェクト構成の説明 |
| `verify_reproducibility.sh` | 同一シードで同一ファイル生成を検証 |
| `.gitignore` | 生成ファイル、キャッシュをGit管理外に |

### src/ - Pythonソースコード

| ファイル | 説明 |
|---------|------|
| `generate.py` | コマンドライン引数を処理し、問題生成とTeX出力を統括 |
| `generators.py` | 3種類の問題生成クラスを実装 |

#### generators.py のクラス

- `LinearEquationGenerator`: 中1一次方程式 (ax + b = c)
- `ProportionalFunctionGenerator`: 中1比例 (x, y値から y = ax)
- `SimultaneousEquationGenerator`: 中2連立方程式 (2x2)

### templates/ - LaTeXテンプレート

| ファイル | 説明 |
|---------|------|
| `problems.tex.j2` | 問題用LaTeXテンプレート（Jinja2形式） |
| `answers.tex.j2` | 解答用LaTeXテンプレート（Jinja2形式） |

#### テンプレート機能

- Noto Sans CJK JP フォント設定
- 日本語禁則処理設定
- 問題データをJinja2変数で埋め込み
- 数式は LaTeX 標準記法

### output/ - 生成ファイル（.gitignoreに含む）

| 拡張子 | 説明 |
|--------|------|
| `.tex` | Pythonスクリプトが生成したLaTeXソース |
| `.pdf` | LuaLaTeXでコンパイルされたPDF |
| `.aux`, `.log` | LaTeX補助ファイル（削除可能） |

## データフロー

```
┌──────────────┐
│ generate.py  │  --seed, --num-problems
└──────┬───────┘
       │
       v
┌──────────────┐
│ generators.py│  問題データ生成（Dict形式）
└──────┬───────┘
       │
       v
┌──────────────┐
│ Jinja2       │  テンプレート＋データ → TeXソース
│ templates/   │
└──────┬───────┘
       │
       v
┌──────────────┐
│ output/      │  .tex ファイル出力
└──────┬───────┘
       │
       v
┌──────────────┐
│ LuaLaTeX     │  TeXソース → PDF
└──────┬───────┘
       │
       v
┌──────────────┐
│ output/      │  .pdf ファイル出力
└──────────────┘
```

## 技術スタック詳細

### Docker環境
- **ベースイメージ**: ubuntu:22.04
- **TeX Live**: texlive-full (LuaLaTeX含む)
- **フォント**: fonts-noto-cjk (Noto Sans CJK JP使用)
- **Python**: 3.10+ (標準搭載)
- **Pythonパッケージ**: jinja2

### LaTeX設定
- **エンジン**: LuaLaTeX（日本語対応、Unicodeネイティブ）
- **日本語パッケージ**: luatexja, luatexja-fontspec
- **数式パッケージ**: amsmath
- **その他**: geometry（余白設定）、enumitem（箇条書き）

### 問題生成
- **言語**: Python 3
- **乱数**: random.Random（シード指定可能）
- **分数処理**: fractions.Fraction（正確な有理数計算）
- **テンプレート**: Jinja2（trim_blocks, lstrip_blocks有効）

## 拡張性

### 新しい問題タイプの追加

1. `src/generators.py` に新しいGeneratorクラスを追加
2. `src/generate.py` で新しいGeneratorをインスタンス化
3. `templates/*.tex.j2` に新しいセクションを追加

### レイアウトの変更

- `templates/*.tex.j2` を編集
- LaTeXパッケージの追加は `\usepackage{}` で

### Docker環境のカスタマイズ

- `Dockerfile` で追加パッケージをインストール
- `docker-compose.yml` で環境変数やボリュームを調整
