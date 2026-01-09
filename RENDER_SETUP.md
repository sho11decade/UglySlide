# Render.com対応改良 - 実装内容

DasaMakerをRender.comでホスティングするための改良を実装しました。

## 📋 実装ファイル一覧

### 新規作成ファイル

| ファイル | 説明 |
|---------|------|
| `Procfile` | Render.com用アプリケーション起動定義 |
| `render.yaml` | Render.com全体設定（YAML形式） |
| `Dockerfile` | Docker コンテナ化設定 |
| `.dockerignore` | Docker ビルド除外設定 |
| `runtime.txt` | Python バージョン指定 |
| `RENDER_DEPLOYMENT.md` | Render.com詳細デプロイメントガイド |
| `uploads/.gitkeep` | uploadsディレクトリ保持ファイル |

### 更新ファイル

| ファイル | 変更内容 |
|---------|---------|
| `web/app.py` | ポート番号を環境変数から読み込み |
| `wsgi.py` | PORT環境変数対応 |
| `.gitignore` | Render.com関連を追加 |

## 🔧 主な改良内容

### 1. ポート設定の柔軟化

```python
# 環境変数PORTを優先、無い場合は5000
port = int(os.getenv('PORT', 5000))
```

**対応:**
- Render.com （ポート: 10000）
- Heroku （ポート: 環境変数PORT）
- ローカル開発 （ポート: 5000）

### 2. Procfile設定

```
web: gunicorn --workers 2 --worker-class sync --bind 0.0.0.0:$PORT --timeout 300 wsgi:app
```

**特徴:**
- $PORT環境変数を自動使用
- 2ワーカーで効率的に動作（メモリ節約）
- 300秒タイムアウト設定

### 3. render.yaml設定

```yaml
services:
  - type: web
    name: dasamaker
    env: python
    plan: free
    healthCheckPath: /api/health
    disk:
      name: upload_storage
      mountPath: /opt/render/project/uploads
      sizeGB: 5
```

**特徴:**
- 自動デプロイ設定
- ヘルスチェック有効
- 永続ストレージ（5GB）の設定

### 4. Docker対応

```dockerfile
FROM python:3.9-slim
EXPOSE 10000
HEALTHCHECK --interval=30s --timeout=3s
CMD ["gunicorn", "--workers", "2", "--worker-class", "sync", "--bind", "0.0.0.0:10000", "--timeout", "300", "wsgi:app"]
```

**メリット:**
- ローカルテストが可能
- どのプラットフォームでも同じ環境で実行
- Render.comのコンテナレジストリにも対応

## 🚀 デプロイ手順

### 簡易版（3ステップ）

```bash
# 1. 変更をコミット
git add .
git commit -m "Render.com対応"
git push origin main

# 2. Render.comダッシュボードで設定
# https://render.com → New Web Service

# 3. GitHubリポジトリを接続してデプロイ
```

### 詳細版

RENDER_DEPLOYMENT.mdを参照（手順を100%網羅）

## 💾 永続ストレージ設定

Render.comのDisk機能を使用：

- **マウントパス**: `/opt/render/project/uploads`
- **容量**: 5GB （無料枠内）
- **自動クリーンアップ**: ダウンロード後に一時ファイル削除

## ✅ テスト方法

### ローカルテスト（Docker）

```bash
# Dockerイメージをビルド
docker build -t dasamaker .

# コンテナを実行
docker run -p 8000:10000 -v $(pwd)/uploads:/app/uploads dasamaker

# http://localhost:8000 でテスト
```

### Render.com本番環境での検証

1. Render.comでデプロイ実行
2. ブラウザで アプリケーション URL にアクセス
3. `/api/health` でヘルスチェック確認

```bash
curl https://dasamaker.onrender.com/api/health
# { "status": "ok", "version": "0.1.0", "timestamp": "2026-01-09T..." }
```

## 📊 パフォーマンス特性

### Render.com フリープラン

| 項目 | 仕様 |
|-----|------|
| **メモリ** | 512MB |
| **CPU** | 共有（0.5vCPU相当） |
| **ディスク** | 5GB |
| **ネットワーク** | 無制限 |
| **非活動停止** | 15分 |
| **月間上限** | 750時間 |

### 推奨構成

```
フリープラン: 開発・テスト用
├─ メモリ: 512MB
├─ ワーカー数: 1-2
└─ 約3台分で月750時間

Starterプラン: 本番用
├─ メモリ: 2GB
├─ ワーカー数: 2-4
└─ 常時起動可能
```

## 🔐 セキュリティ

### 自動設定

- ✅ HTTPS/TLS （自動設定）
- ✅ SSL証明書 （自動更新）
- ✅ セキュリティヘッダー （既実装）
- ✅ レート制限 （IP毎10リクエスト/時間）

### 推奨設定

- ✅ カスタムドメイン設定
- ✅ 環境変数の保護
- ✅ ログの監視

## 🐛 トラブルシューティング

### よくある問題

#### 1. ビルドエラー

```
Error: Python 3.x not found
```

**解決:**
```bash
runtime.txt に Python 3.9 を指定
```

#### 2. ポート接続エラー

```
Error: Cannot bind to port
```

**解決:**
```python
port = int(os.getenv('PORT', 5000))  # 既に実装済み
```

#### 3. ファイルアップロード失敗

```
Error: No space left on device
```

**解決:**
- Render.comダッシュボード → Disks でサイズ確認
- `uploads/.gitkeep` ファイル確認

#### 4. タイムアウトエラー

```
Error: Worker timeout
```

**解決:**
```
Procfile の timeout を 300秒 に設定（既に実装済み）
```

## 📝 環境変数参考

### 本番環境（Render.com）

```
FLASK_ENV=production
PYTHONUNBUFFERED=true
```

### ローカル開発

```bash
export FLASK_ENV=development
export PORT=5000
python -m web.app
```

## 🎯 次のステップ

1. **GitHub リポジトリを準備**
   - 最新コードをプッシュ

2. **Render.com アカウント作成**
   - https://render.com

3. **デプロイ実行**
   - RENDER_DEPLOYMENT.md の手順に従う

4. **本番環境テスト**
   - ファイルアップロード機能確認
   - ダウンロード機能確認

## 📚 参考リンク

- [Render.com ドキュメント](https://render.com/docs)
- [Gunicorn 設定](https://docs.gunicorn.org/)
- [Flask デプロイメント](https://flask.palletsprojects.com/deployment/)

---

**Render.comでの本番運用を推奨します！ 🚀**
