# UglySlide

🎨 PowerPoint プレゼンテーションを意図的に「ダサく」変身させるユーティリティ

## 概要

このアプリケーションは、既存のPPTファイルを解析し、そのデザインや内容に基づいて「ダサい」プレゼンテーションを自動生成します。ユーザーは自分のPPTファイルをアップロードするだけで、ユーモラスで風刺的なダサいバージョンのプレゼンテーションを受け取ることができます。

## 特徴

- ✨ **自動デザイン解析**: フォント、色、レイアウト、アニメーションを検出
- 🎭 **ダサいデザイン生成**: 意図的に不適切なフォント（Comic Sans、Papyrus）やネオン色を適用
- 📝 **風刺的なコンテンツ変換**: テキストを冗長化し、古い企業用語やランダムな雑学を挿入
- 🎚️ **調整可能なレベル**: ダサさの強度を1～10レベルで制御
- 🌐 **Web UI**: Flask ベースの直感的なインターフェース
- 📊 **設計意識向上**: ユーモアを通じてプレゼンテーション改善点を示唆

## 技術スタック

- **バックエンド**: Python 3.8+
- **フレームワーク**: Flask 3.0
- **PPT処理**: python-pptx 0.6.23
- **テスト**: pytest
- **フロントエンド**: HTML5, CSS3, Vanilla JavaScript

## インストール

### 前提条件

- Python 3.8以上
- pip

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/DasaMaker.git
cd DasaMaker

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

## 使用方法

### Web UIの起動

```bash
# Flask アプリケーションを実行
python -m web.app

# ブラウザで http://localhost:5000 にアクセス
```

### ステップ

1. **ファイルをアップロード**: PPTX ファイルを選択またはドラッグ＆ドロップ
2. **ダサさレベルを設定**: デザイン強度（1-10）とコンテンツ変換強度（1-10）を調整
3. **生成**: 「ダサイ版を生成する!」ボタンをクリック
4. **ダウンロード**: 生成されたPPTXファイルをダウンロード

## プロジェクト構造

```
DasaMaker/
├── src/
│   ├── __init__.py
│   ├── ppt_analyzer.py       # PPT解析・デザイン要素抽出
│   ├── taco_generator.py     # ダサいデザイン生成ロジック
│   └── content_transformer.py # 風刺的なコンテンツ変換
├── web/
│   ├── app.py                # Flask アプリケーション
│   ├── templates/
│   │   └── index.html        # メインUI
│   └── static/
│       ├── style.css         # スタイル
│       └── script.js         # フロントエンド ロジック
├── tests/
│   └── test_modules.py       # ユニット・統合テスト
├── samples/                  # サンプルPPTファイル
├── requirements.txt          # Python依存関係
├── pyproject.toml           # プロジェクト設定
└── README.md                # このファイル
```

## API エンドポイント

### POST `/api/process`

プレゼンテーションを処理してダサいバージョンを生成

**クエリパラメータ:**
- `design_level` (1-10, デフォルト=7): デザインのダサさレベル
- `content_level` (1-10, デフォルト=7): コンテンツ変換の強度

**リクエスト:**
```bash
curl -X POST -F "file=@presentation.pptx" \
  "http://localhost:5000/api/process?design_level=7&content_level=7"
```

**レスポンス:**
```json
{
  "success": true,
  "filename": "presentation_TACKY.pptx",
  "analysis": {
    "total_slides": 10,
    "fonts_found": 5,
    "colors_found": 8,
    "animations_found": 12
  }
}
```

### GET `/api/download/<filename>`

生成されたPPTXファイルをダウンロード

### GET `/api/health`

ヘルスチェック

## テスト

```bash
# すべてのテストを実行
pytest

# カバレッジレポート付き
pytest --cov=src tests/

# HTMLカバレッジレポート
pytest --cov=src --cov-report=html tests/
# report をブラウザで開く: htmlcov/index.html
```

## デザイン変換の仕組み

### 1. PPT解析 (`ppt_analyzer.py`)
- スライドレイアウトを検出
- フォントと色を抽出
- アニメーションをカウント
- テキスト要素を収集

### 2. ダサいデザイン生成 (`taco_generator.py`)

**ダサさレベルに応じた変換:**

| レベル | 変換内容 |
|--------|----------|
| 1-2 | 基本的な色変更 |
| 3-4 | Comic Sans や Papyrus への置換 |
| 5-6 | ネオン色グラデーション適用 |
| 7-8 | マルチカラーグラデーション、フォント変更 |
| 9-10 | 極度のグラデーション、全要素過剰装飾 |

**使用するタッキーフォント:**
- Comic Sans MS
- Papyrus
- Impact
- Curlz MT
- Jokerman

**ネオンカラーパレット:**
- ホットピンク `(255, 0, 127)`
- シアン `(0, 255, 255)`
- ライムグリーン `(0, 255, 0)`
- ほか多数

**グラデーション過激化機能:**
- **レベル5-6**: 2色のネオングラデーション
- **レベル7-8**: 3-4色のマルチカラーグラデーション
- **レベル9-10**: 全ネオンカラー使用の極度グラデーション

### 3. コンテンツ変換 (`content_transformer.py`)

**変換ルール:**

| レベル | 変換タイプ |
|--------|----------|
| 1-3 | 冗長な冒頭フレーズを追加 |
| 4-6 | 古い企業用語を挿入 |
| 5-7 | ランダムな雑学事実を追加 |
| 7-9 | 皮肉的なトーンを追加 |
| 9-10 | 重要な言葉を繰り返す強調 |

**追加される冗長フレーズ例:**
> "It is imperative to note that..."
> "Synergistically speaking..."
> "From a holistic perspective..."

**挿入される古い企業用語:**
> "leverage synergies", "circle back", "deep dive", "boil the ocean"

## トラブルシューティング

### ファイルがアップロードできない

- ファイルサイズが50MB以下であることを確認
- ファイル形式が `.pptx` であることを確認（`.ppt` は非対応）
- ブラウザのキャッシュをクリアしてみてください

### 処理がハングする

- 大きなプレゼンテーション（100+スライド）の場合、処理に時間がかかることがあります
- ブラウザコンソール（F12キー）でエラーを確認してください
- サーバーログで詳細な情報を確認してください

### ダウンロードに失敗する

- ブラウザのダウンロード設定を確認
- ファイアウォールやVPNがブロックしていないか確認
- サーバーのディスク容量を確認

## デプロイメント

### 本番環境への展開

#### 前提条件
- Python 3.8以上
- Gunicorn（本番用WSGIサーバー）
- 十分なディスク容量（一時ファイル用）

#### セットアップ手順

```bash
# 依存関係のインストール
pip install -r requirements.txt
pip install gunicorn

# 本番環境での実行
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 web.app:app
```

#### Nginx設定例

```nginx
upstream dasama_app {
    server localhost:5000;
}

server {
    listen 80;
    server_name yourdomain.com;
    client_max_body_size 50M;

    location / {
        proxy_pass http://dasama_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
    }

    location /static {
        alias /path/to/DasaMaker/web/static;
        expires 30d;
    }
}
```

#### Docker対応

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "web.app:app"]
```

### セキュリティ設定

- HTTPS/TLSを必ず有効化してください
- CSRFトークンは自動的に処理されます
- レート制限が実装されています（1時間あたり10リクエスト/IP）
- ファイルアップロードのバリデーションが厳密です

### パフォーマンス最適化

- 複数ワーカー（Gunicorn）でスケーリング可能
- 一時ファイルの自動クリーンアップ機能
- ファイルサイズの制限（50MB）
- タイムアウト設定（5分）

## トラブルシューティング

### ファイルがアップロードできない

- ファイルサイズが50MB以下であることを確認
- ファイル形式が `.pptx` であることを確認（`.ppt` は非対応）
- ブラウザのキャッシュをクリアしてみてください

### 処理がハングする

- 大きなプレゼンテーション（100+スライド）の場合、処理に時間がかかることがあります
- ブラウザコンソール（F12キー）でエラーを確認してください
- サーバーログで詳細な情報を確認してください

### ダウンロードに失敗する

- ブラウザのダウンロード設定を確認
- ファイアウォールやVPNがブロックしていないか確認
- サーバーのディスク容量を確認

## ライセンス

MIT License

## 貢献

改善提案やバグ報告は [GitHub Issues](https://github.com/yourusername/DasaMaker/issues) でお願いします。

## 参考資料

- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ProjectProposal.md](./ProjectProposal.md) - 詳細な機能仕様

---

**楽しくデザイン意識を高めよう!** 🚀