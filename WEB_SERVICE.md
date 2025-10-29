# Webサービス使用ガイド

## 概要

ブラウザから数学演習問題PDFを生成・ダウンロードできるWebアプリケーションです。

## 特徴

- 🌐 ブラウザベースのUI
- 📊 シード値と問題数をカスタマイズ可能
- 📥 問題用PDF・解答用PDFを個別またはまとめてダウンロード
- 🎨 モダンなデザイン
- ⚡ Flask + LuaLaTeX によるバックエンド

## クイックスタート

### 1. Dockerイメージのビルド

```bash
docker compose build
```

### 2. Webサーバーの起動

```bash
docker compose up web
```

または、バックグラウンドで起動:

```bash
docker compose up -d web
```

### 3. ブラウザでアクセス

```
http://localhost:5000
```

## 使い方

### Webインターフェース

1. **ブラウザを開く**: `http://localhost:5000` にアクセス

2. **パラメータを設定**:
   - **乱数シード**: 1〜999999（デフォルト: 12345）
   - **問題数**: 各セクション1〜20問（デフォルト: 5）
   - **生成タイプ**: 両方/問題のみ/解答のみ

3. **PDF生成**: 「PDF生成」ボタンをクリック

4. **ダウンロード**: 生成完了後、ダウンロードリンクが表示される

### 生成時間

- 初回: 約20〜30秒（LaTeXコンパイル含む）
- 2回目以降: 約15〜25秒

## API エンドポイント

### POST /generate

PDF生成エンドポイント

**パラメータ（Form Data）:**
```
seed: integer (1-999999)
num_problems: integer (1-20)
pdf_type: string ("problems" | "answers" | "both")
```

**レスポンス（JSON）:**
```json
{
  "success": true,
  "seed": 12345,
  "num_problems": 5,
  "files": [
    {
      "name": "problems",
      "filename": "problems_seed12345.pdf",
      "url": "/download/problems_seed12345.pdf"
    },
    {
      "name": "answers",
      "filename": "answers_seed12345.pdf",
      "url": "/download/answers_seed12345.pdf"
    }
  ]
}
```

**エラーレスポンス:**
```json
{
  "error": "Error message"
}
```

### GET /download/<filename>

PDF ダウンロードエンドポイント

**例:**
```
GET /download/problems_seed12345.pdf
```

### GET /health

ヘルスチェックエンドポイント

**レスポンス:**
```json
{
  "status": "ok"
}
```

## curlでのAPI使用例

### PDF生成

```bash
# 両方のPDFを生成
curl -X POST http://localhost:5000/generate \
  -F "seed=12345" \
  -F "num_problems=5" \
  -F "pdf_type=both"

# 問題のみ生成
curl -X POST http://localhost:5000/generate \
  -F "seed=54321" \
  -F "num_problems=10" \
  -F "pdf_type=problems"
```

### PDFダウンロード

```bash
curl -O http://localhost:5000/download/problems_seed12345.pdf
curl -O http://localhost:5000/download/answers_seed12345.pdf
```

## Docker Composeコマンド

### サーバー起動

```bash
# フォアグラウンド
docker compose up web

# バックグラウンド
docker compose up -d web
```

### ログ確認

```bash
docker compose logs -f web
```

### サーバー停止

```bash
docker compose down
```

### サーバー再起動

```bash
docker compose restart web
```

## ディレクトリ構成

```
src/
├── app.py              # Flaskアプリケーション
├── generate.py         # CLIツール（従来版）
├── generators.py       # 問題生成ロジック
└── templates/
    └── index.html      # Webインターフェース
```

## 開発モード

### ホットリロード有効

```bash
# docker-compose.ymlのFLASK_ENV=developmentで有効化済み
docker compose up web
# コード変更時に自動リロード
```

### デバッグ

```bash
# ログをリアルタイムで確認
docker compose logs -f web
```

## プロダクション環境での使用

### 環境変数の変更

`docker-compose.yml` を編集:

```yaml
environment:
  - FLASK_ENV=production
  - FLASK_DEBUG=0
```

### Gunicornの使用（推奨）

`requirements.txt` を作成:
```
flask
gunicorn
jinja2
```

`Dockerfile` を更新:
```dockerfile
RUN pip3 install --no-cache-dir -r requirements.txt
```

起動コマンドを変更:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

## トラブルシューティング

### ポート5000が使用中

別のポートを使用:

`docker-compose.yml`:
```yaml
ports:
  - "8080:5000"
```

アクセス: `http://localhost:8080`

### PDFが生成されない

1. **LuaLaTeXのインストール確認**:
   ```bash
   docker compose run --rm web lualatex --version
   ```

2. **ログ確認**:
   ```bash
   docker compose logs web
   ```

3. **パーミッション確認**:
   ```bash
   ls -la output/
   ```

### メモリ不足

`docker-compose.yml` にメモリ制限を追加:

```yaml
web:
  deploy:
    resources:
      limits:
        memory: 2G
```

## パフォーマンス最適化

### 1. コンパイル回数の削減

`src/app.py` の `compile_tex_to_pdf` で2回→1回に変更（参照が不要な場合）

### 2. 出力ディレクトリのクリーンアップ

古いPDFファイルを定期削除:

```bash
# 1日以上前のファイルを削除
find output/ -name "*.pdf" -mtime +1 -delete
```

### 3. キャッシュの活用

同じシードでの再生成をキャッシュ（要実装）

## セキュリティ考慮事項

1. **ファイルアップロード制限**: 最大16MB（設定済み）
2. **パラメータ検証**: シード値、問題数の範囲チェック（実装済み）
3. **タイムアウト**: LaTeXコンパイルは60秒でタイムアウト（設定済み）
4. **ファイル名サニタイズ**: ダウンロード時のパストラバーサル対策（要実装）

## まとめ

Webサービス版の利点:
- ✅ ブラウザから簡単にアクセス
- ✅ CLIコマンド不要
- ✅ 直感的なUI
- ✅ 即座にダウンロード可能
- ✅ 複数ユーザーでの共有が容易

従来のCLI版との併用も可能です。
