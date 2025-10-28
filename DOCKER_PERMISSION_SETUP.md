# Docker権限設定ガイド

## 問題: Permission Denied エラー

Dockerコマンド実行時に以下のエラーが出る場合：

```
permission denied while trying to connect to the Docker daemon socket
```

## 原因

ユーザーが `docker` グループに所属していないため、Dockerデーモンへのアクセスが拒否されています。

## 解決方法

### 1. ユーザーをdockerグループに追加

```bash
sudo usermod -aG docker $USER
```

### 2. グループ変更を反映

以下のいずれかの方法で変更を反映：

#### 方法A: ログアウト・ログイン（推奨）
```bash
# 一度ログアウトして再度ログイン
exit
# または
# システムを再起動
```

#### 方法B: newgrpコマンド（一時的）
```bash
newgrp docker
```

#### 方法C: 現在のシェルで確認
```bash
# 現在のグループを確認
groups
# 出力に "docker" が含まれていればOK
```

### 3. 動作確認

```bash
# Dockerが動作するか確認
docker ps

# イメージビルド
docker compose build

# PDF生成テスト
make docker-build
```

## WSL (Windows Subsystem for Linux) の場合

WSLでは追加の設定が必要な場合があります：

### Docker Desktopを使用している場合

1. Docker Desktopの設定を開く
2. "Resources" → "WSL Integration"
3. 使用しているWSLディストリビューションを有効化

### Docker Daemonの起動確認

```bash
# Docker Daemonが起動しているか確認
sudo service docker status

# 起動していない場合
sudo service docker start
```

## 手動テスト手順

権限設定後、以下の手順でテストを実行：

```bash
# 1. 権限確認
groups | grep docker

# 2. Docker動作確認
docker --version
docker compose version

# 3. イメージビルド（初回は10-20分かかる）
docker compose build

# 4. PDF生成テスト
make docker-build SEED=12345

# 5. 生成確認
ls -lh output/
# problems.pdf と answers.pdf が存在すればOK
```

## トラブルシューティング

### 依然としてpermission deniedが出る場合

```bash
# Docker socketの権限確認
ls -la /var/run/docker.sock

# 出力例:
# srw-rw---- 1 root docker 0 Oct 29 07:28 /var/run/docker.sock

# dockerグループへの所属を再確認
id -nG | grep docker
```

### グループが反映されない場合

```bash
# 完全に新しいシェルセッションを開始
exec su -l $USER

# 再度確認
groups
```

## Docker不要の代替方法

Dockerの権限問題が解決できない場合、ローカル環境にTeX Liveをインストール：

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y texlive-full texlive-luatex \
                        texlive-lang-japanese fonts-noto-cjk

# Python依存関係
pip3 install jinja2

# PDF生成（Dockerなし）
make build SEED=12345
```

## 確認済み環境

このプロジェクトは以下の環境でテスト済みです：

- ✅ Python 3.12.3
- ✅ Jinja2インストール済み
- ✅ TeXファイル生成動作確認済み
- ⚠️ Docker環境は権限設定が必要

## まとめ

1. `sudo usermod -aG docker $USER` でグループ追加
2. ログアウト・ログイン or `newgrp docker` で反映
3. `docker compose build` でイメージビルド
4. `make docker-build` でPDF生成

権限設定後は、Dockerコンテナ内で完全に再現可能なPDF生成が可能になります。
