# DasaMaker 本番環境デプロイメントガイド

本番環境でDasaMakerを安全かつ効率的に運用するためのガイドです。

## 前提条件

- Linux サーバー（Ubuntu 20.04 LTS 推奨）
- Python 3.8以上
- Nginx または Apache
- SSL証明書（Let's Encrypt推奨）
- 最低1GB RAM、10GB ストレージ

## セットアップ手順

### 1. システムパッケージのインストール

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx curl
```

### 2. アプリケーションのセットアップ

```bash
# ユーザー作成
sudo useradd -m -s /bin/bash dasamaker
sudo su - dasamaker

# リポジトリのクローン
git clone https://github.com/yourusername/DasaMaker.git
cd DasaMaker

# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate

# 本番用依存関係のインストール
pip install -r requirements-prod.txt
```

### 3. 環境変数の設定

```bash
cp .env.example .env
nano .env  # 環境に合わせて編集
```

### 4. Systemdサービスの設定

`/etc/systemd/system/dasamaker.service` を作成：

```ini
[Unit]
Description=DasaMaker Flask Application
After=network.target

[Service]
Type=notify
User=dasamaker
WorkingDirectory=/home/dasamaker/DasaMaker
Environment="PATH=/home/dasamaker/DasaMaker/venv/bin"
ExecStart=/home/dasamaker/DasaMaker/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 300 \
    --access-logfile /var/log/dasamaker/access.log \
    --error-logfile /var/log/dasamaker/error.log \
    wsgi:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# ログディレクトリの作成
sudo mkdir -p /var/log/dasamaker
sudo chown dasamaker:dasamaker /var/log/dasamaker

# サービスの有効化と開始
sudo systemctl daemon-reload
sudo systemctl enable dasamaker
sudo systemctl start dasamaker
```

### 5. Nginxの設定

`/etc/nginx/sites-available/dasamaker` を作成：

```nginx
upstream dasamaker_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # HTTPからHTTPSへリダイレクト
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL証明書（Let's Encrypt）
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL設定
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # クライアント制限
    client_max_body_size 50M;
    client_body_timeout 300;

    # ロギング
    access_log /var/log/nginx/dasamaker_access.log;
    error_log /var/log/nginx/dasamaker_error.log;

    # セキュリティヘッダー
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://dasamaker_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    # 静的ファイル
    location /static {
        alias /home/dasamaker/DasaMaker/web/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# サイトの有効化
sudo ln -s /etc/nginx/sites-available/dasamaker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL証明書の取得（Let's Encrypt）

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### 7. 自動更新の設定

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## 監視とメンテナンス

### ログの確認

```bash
# アプリケーションログ
sudo tail -f /var/log/dasamaker/error.log
sudo tail -f /var/log/dasamaker/access.log

# Nginxログ
sudo tail -f /var/log/nginx/dasamaker_error.log
```

### ディスク容量の管理

```bash
# 一時ファイルの定期削除
sudo crontab -e
# 毎日午前3時に古いファイルを削除
0 3 * * * find /home/dasamaker/DasaMaker/uploads -type f -mtime +1 -delete
```

### サービスの再起動

```bash
sudo systemctl restart dasamaker
```

## バックアップ

```bash
# アップロードフォルダのバックアップ
tar -czf dasamaker_uploads_$(date +%Y%m%d).tar.gz uploads/

# 設定ファイルのバックアップ
cp .env .env.backup
```

## トラブルシューティング

### サービスが起動しない

```bash
sudo systemctl status dasamaker
sudo journalctl -u dasamaker -n 50
```

### ファイルアップロードエラー

- ディスク容量の確認：`df -h`
- パーミッションの確認：`ls -la uploads/`
- Nginxの制限確認：`client_max_body_size`

### メモリ不足

```bash
# Gunicownワーカー数の調整
# /etc/systemd/system/dasamaker.service で workers を減らす
--workers 2  # デフォルトの4から減らす
```

## セキュリティベストプラクティス

✅ HTTPS/TLSを有効化
✅ ファイアウォール設定（ポート80, 443のみ）
✅ 定期的なセキュリティアップデート
✅ ログの監視
✅ ファイルサイズ制限の設定
✅ レート制限の有効化

## パフォーマンスチューニング

### 推奨設定

```nginx
# Nginx バッファサイズ
proxy_buffer_size 128k;
proxy_buffers 4 256k;

# キープアライブ
keepalive_timeout 65;
keepalive_requests 100;
```

### 負荷テスト

```bash
# Apache Benchを使用したテスト
ab -n 100 -c 10 https://yourdomain.com/
```

## サポート

問題が発生した場合は、[GitHub Issues](https://github.com/yourusername/DasaMaker/issues) を参照してください。
