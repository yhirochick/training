# Docker 使用ガイド

## Docker環境でのPDF生成完全ガイド

このガイドでは、Dockerを使用してPDFを生成する手順を詳しく説明します。

## 前提条件

- Docker がインストールされていること
- Docker Compose がインストールされていること

### Dockerのインストール確認

```bash
docker --version
docker compose version
```

## ステップ1: Dockerイメージのビルド

初回のみ実行が必要です（約5-10分かかります）。

```bash
docker compose build
```

このコマンドは以下を実行します:
- Ubuntu 22.04ベースイメージの取得
- TeX Live（LuaLaTeX含む）のインストール
- Noto CJKフォントのインストール
- Python 3とJinja2のインストール

### ビルド中のメッセージ例

```
[+] Building 300.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/5] FROM docker.io/library/ubuntu:22.04
 => [2/5] RUN apt-get update && apt-get install -y texlive-full...
 => [3/5] RUN pip3 install --no-cache-dir jinja2
...
```

## ステップ2: PDF生成

### 基本的な生成（デフォルトシード: 12345）

```bash
make docker-build
```

このコマンドは以下を実行します:
1. Dockerコンテナ起動
2. Pythonスクリプトで問題生成（problems.tex, answers.tex）
3. LuaLaTeXでPDFコンパイル（2回実行で目次・参照解決）
4. 出力ファイルを `output/` に配置
5. コンテナ自動終了

### カスタムシードで生成

```bash
make docker-build SEED=54321
```

### 出力ファイルの確認

```bash
ls -lh output/
# problems.pdf  - 問題用PDF
# answers.pdf   - 解答用PDF
# problems.tex  - 問題用LaTeXソース
# answers.tex   - 解答用LaTeXソース
# *.aux, *.log  - LaTeX補助ファイル
```

## ステップ3: PDFの表示

### Linuxの場合

```bash
# evince（GNOME）
evince output/problems.pdf &

# okular（KDE）
okular output/problems.pdf &

# Firefox
firefox output/problems.pdf &
```

### WSL（Windows Subsystem for Linux）の場合

```bash
# Windowsの既定のPDFビューアで開く
explorer.exe output/problems.pdf
explorer.exe output/answers.pdf
```

### macOSの場合

```bash
open output/problems.pdf
```

## Docker詳細コマンド

### コンテナ内でシェルを起動

```bash
docker compose run --rm latex-builder bash
```

コンテナ内で自由にコマンド実行可能:

```bash
# 問題生成
python3 src/generate.py --seed 99999 --num-problems 10

# TeXコンパイル
lualatex -output-directory=output output/problems.tex

# フォント確認
fc-list | grep Noto

# 終了
exit
```

### 手動でのPDF生成（コンテナ内）

```bash
docker compose run --rm latex-builder bash

# コンテナ内で実行
cd /workspace
python3 src/generate.py --seed 12345
lualatex -output-directory=output output/problems.tex
lualatex -output-directory=output output/problems.tex  # 2回目
lualatex -output-directory=output output/answers.tex
lualatex -output-directory=output output/answers.tex   # 2回目
exit
```

### 生成ファイルのクリーンアップ

```bash
# Docker環境でクリーンアップ
make docker-clean

# または手動で
rm -f output/*.pdf output/*.tex output/*.aux output/*.log
```

## トラブルシューティング

### 1. 権限エラー（permission denied）

**問題**: `permission denied while trying to connect to the Docker daemon socket`

**解決策**:
```bash
# ユーザーをdockerグループに追加
sudo usermod -aG docker $USER

# 再ログイン（またはシステム再起動）
# その後、再度実行
docker compose build
```

### 2. ディスク容量不足

**問題**: `no space left on device`

**解決策**:
```bash
# 未使用のDockerイメージ削除
docker system prune -a

# ディスク使用量確認
docker system df
```

### 3. ビルドが遅い

**原因**: TeX Live（約4GB）のダウンロードとインストール

**対策**:
- 初回ビルドは時間がかかります（10-20分）
- 2回目以降はキャッシュが効きます
- ネットワーク環境を確認

### 4. 生成されたPDFが文字化け

**原因**: フォントが正しくインストールされていない

**解決策**:
```bash
# イメージを再ビルド（キャッシュなし）
docker compose build --no-cache

# コンテナ内でフォント確認
docker compose run --rm latex-builder fc-list | grep Noto
```

### 5. output/ に何も生成されない

**確認事項**:
```bash
# Pythonスクリプトが正常か確認
docker compose run --rm latex-builder python3 src/generate.py --seed 12345

# TeXファイルが生成されているか確認
ls output/*.tex

# LaTeXのエラーログ確認
cat output/problems.log
```

## 高度な使用法

### カスタムDockerイメージのタグ付け

```bash
# イメージをビルドしてタグ付け
docker compose build
docker tag training-latex-builder:latest my-math-generator:v1.0
```

### 複数バージョンの管理

```bash
# 異なるシードで複数生成
make docker-build SEED=12345
mv output/problems.pdf output/problems_seed12345.pdf
mv output/answers.pdf output/answers_seed12345.pdf

make docker-build SEED=54321
mv output/problems.pdf output/problems_seed54321.pdf
mv output/answers.pdf output/answers_seed54321.pdf
```

### バックグラウンド実行

```bash
# バックグラウンドでビルド
make docker-build SEED=12345 &

# 進行状況確認
jobs
```

## Docker環境の削除

プロジェクトが不要になった場合:

```bash
# イメージ削除
docker compose down --rmi all

# ボリューム含めて完全削除
docker compose down --rmi all --volumes

# 生成ファイル削除
rm -rf output/*
```

## 参考情報

### Dockerイメージサイズ

```bash
docker images | grep training
# 約5-6GB（TeX Live含む）
```

### コンテナのリソース使用量

```bash
# 実行中のコンテナ確認
docker compose ps

# リソース使用量確認
docker stats
```

## まとめ

Docker環境を使用することで:
- ✅ 環境差異を完全に排除
- ✅ ローカルにTeX Liveをインストール不要
- ✅ 同一のPDFを再現可能
- ✅ クリーンな環境で実行

TeX Liveのインストールが不要なため、初心者にも推奨される方法です。
