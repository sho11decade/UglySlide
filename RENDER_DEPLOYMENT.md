# Render.com デプロイメントガイド

DasaMakerをRender.comでホスティングするための完全ガイドです。

## 必要な準備

- GitHubアカウント
- Render.comアカウント
- DasaMakerのGitHubリポジトリ

## ステップ1: GitHub リポジトリの準備

```bash
# 最新の変更をプッシュ
git add .
git commit -m "Render.com対応"
git push origin main
```

## ステップ2: Render.comでの設定

### 2.1 新しいWebサービスを作成

1. [Render.com](https://render.com)にログイン
2. ダッシュボードで「New +」 → 「Web Service」をクリック
3. GitHubリポジトリを接続
   - 「Connect a repository」をクリック
   - DasaMakerリポジトリを選択
   - 「Connect」をクリック

### 2.2 デプロイ設定

| 設定項目 | 値 |
|---------|---|
| **Name** | dasamaker （任意） |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --workers 2 --worker-class sync --bind 0.0.0.0:$PORT --timeout 300 wsgi:app` |
| **Instance Type** | Free （開始時） |
| **Auto-deploy** | Yes |

### 2.3 環境変数の設定

「Environment」セクションで以下を追加：

| キー | 値 |
|-----|---|
| FLASK_ENV | production |
| PYTHONUNBUFFERED | true |

### 2.4 ディスク設定（永続ストレージ）

「Disk」セクションで以下を設定：

| 項目 | 値 |
|-----|---|
| **Name** | upload_storage |
| **Mount Path** | /opt/render/project/uploads |
| **Size** | 5 GB |

## ステップ3: デプロイ実行

1. すべて設定したら「Create Web Service」をクリック
2. ビルドログを確認して、デプロイが成功するのを待ちます
3. デプロイ完了後、アプリケーションURLがダッシュボードに表示されます

```
例: https://dasamaker.onrender.com
```

## ステップ4: アプリケーション動作確認

ブラウザで以下のURLにアクセス：

```
https://dasamaker.onrender.com/
```

ヘルスチェック：

```
https://dasamaker.onrender.com/api/health
```

## トラブルシューティング

### ビルドが失敗する場合

**ログを確認:**
- Render.comダッシュボード → 「Logs」タブ
- 「Build」または「Deploy」ログを確認

**よくある問題:**

1. **Python バージョン エラー**
   - `runtime.txt` が正しく設定されているか確認
   - Python 3.9推奨

2. **依存関係エラー**
   - `requirements.txt` にすべての依存関係が含まれているか確認
   - `pip list > requirements.txt` で更新

3. **メモリ不足エラー**
   - フリープランのメモリ制限（512MB）の可能性
   - 有料プラン（Starter）へのアップグレードを検討

### アプリが起動しない場合

**ログを確認:**

```bash
# Render.comダッシュボード → "Logs" → "Runtime logs"
```

**一般的な原因:**

| 問題 | 解決策 |
|------|-------|
| ImportError | `pip install -r requirements.txt` を確認 |
| ポートエラー | `$PORT` 環境変数が使用されているか確認 |
| パーミッション | uploads フォルダに書き込み権限があるか確認 |

### ファイルアップロードが失敗する場合

1. ディスク設定が正しいか確認
   - Render.comダッシュボード → 「Disks」で確認
   - マウントパス: `/opt/render/project/uploads`

2. 容量を確認
   - 使用容量が制限を超えていないか確認
   - 必要に応じてディスクサイズを増やす

## 料金について

### フリープラン（Free Tier）

- 無料でホスティング可能
- **制限:**
  - メモリ: 512MB
  - CPU: 共有
  - ディスク: 5GB （購入可能）
  - 15分間の非活動で停止される
  - 月合計時間: 750時間（約3台分）

### Starter プラン

- 月額$7から
- **メリット:**
  - 常時起動
  - 2GB メモリ
  - 優先サポート

## パフォーマンス最適化

### フリープランでの最適化

```bash
# Procfile のワーカー数を削減（メモリ節約）
gunicorn --workers 1 --worker-class sync --bind 0.0.0.0:$PORT --timeout 300 wsgi:app
```

### 推奨設定

| パラメータ | フリー | Starter |
|----------|-------|---------|
| Workers | 1-2 | 2-4 |
| Timeout | 300秒 | 300-600秒 |
| Memory | 512MB | 2GB |

## カスタムドメイン設定

### カスタムドメイン追加

1. Render.comダッシュボード → サービス選択
2. 「Settings」 → 「Custom Domain」
3. ドメイン名を入力
4. DNS設定を実施（プロバイダーで）

### DNS設定例（Namecheap）

```
Type: CNAME
Name: www
Value: dasamaker.onrender.com
TTL: 3600
```

## セキュリティ設定

### HTTPS （自動）

- Render.comが自動でHTTPS化
- SSL証明書は無料で自動更新

### セキュリティヘッダー

既に実装されています：
- X-Content-Type-Options: nosniff
- X-Frame-Options: SAMEORIGIN
- X-XSS-Protection: 1; mode=block

## モニタリング

### ログの確認

```bash
# リアルタイムログ表示
Render.comダッシュボード → "Logs" → "Runtime logs"
```

### メトリクス確認

- CPU使用率
- メモリ使用率
- リクエスト数

## 問題が発生した場合

### デバッグ手順

1. **ログを確認**
   - Render.com ダッシュボード → 「Logs」

2. **ローカルで動作確認**
   ```bash
   python -m web.app
   ```

3. **Render.comサポートに連絡**
   - https://render.com/support

## 更新とデプロイ

### 自動デプロイ（Git連携）

```bash
# GitHubに変更をプッシュ
git push origin main
# Render.comが自動的に検出して再デプロイ
```

### 手動再デプロイ

1. Render.comダッシュボード
2. 「Manual Deploy」をクリック
3. ブランチ選択
4. 「Deploy latest commit」をクリック

## コスト削減のコツ

- フリープランから開始
- 非活動時間の停止を許容
- 定期的にメモリ使用量を確認
- 不要な依存関係を削除

---

**デプロイ成功を祈ります！ 🚀**
