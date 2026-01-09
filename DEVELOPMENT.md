# DasaMaker - Quick Start Guide

これは DasaMaker の実行・開発を始めるためのガイドです。

## インストール

```bash
# 依存関係をインストール
pip install -r requirements.txt

# テスト依存関係も含める場合
pip install -r requirements.txt pytest pytest-cov
```

## Web UIで使用

```bash
# Flask アプリケーションを起動
python -m web.app

# ブラウザで http://localhost:5000 にアクセス
```

## コマンドラインで使用

```bash
# 基本的な使用方法
python main.py input.pptx

# 出力ファイルを指定
python main.py input.pptx -o output.pptx

# ダサさレベルを指定 (1-10)
python main.py input.pptx -d 9 -c 8

# 詳細ログを表示
python main.py input.pptx -v
```

## テストの実行

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/test_modules.py

# カバレッジレポート付き
pytest --cov=src tests/

# HTMLカバレッジレポート生成
pytest --cov=src --cov-report=html tests/
```

## プロジェクト構造

```
src/
  - ppt_analyzer.py      : PPT解析とデザイン要素抽出
  - taco_generator.py    : ダサいデザイン生成
  - content_transformer.py: 風刺的なコンテンツ変換

web/
  - app.py               : Flask Webアプリケーション
  - templates/index.html : UIテンプレート
  - static/              : CSS/JavaScriptファイル

tests/
  - test_modules.py      : ユニット・統合テスト

main.py                  : CLIエントリーポイント
config.py               : アプリケーション設定
```

## 開発メモ

### ダサさレベル (1-10)

- **1-2**: 基本的な色変更のみ
- **3-4**: タッキーなフォント（Comic Sans等）に置換
- **5-6**: ネオン色を適用、背景色を追加
- **7-8**: フォントサイズ増加、太字・斜体化
- **9-10**: すべての要素に過剰な装飾

### コンテンツ変換レベル (1-10)

- **1-3**: 冗長な冒頭フレーズを追加
- **4-6**: 古い企業用語を挿入
- **5-7**: ランダムな雑学を追加
- **7-9**: 皮肉的なトーンを追加
- **9-10**: 言葉の繰り返しで強調

## トラブルシューティング

### ImportError: No module named 'pptx'

```bash
pip install python-pptx
```

### ファイルが大きすぎる

Web UIの上限は50MB。コマンドラインではより大きなファイルも処理可能。

```bash
python main.py large_file.pptx
```

## 参考資料

- [python-pptx ドキュメント](https://python-pptx.readthedocs.io/)
- [Flask ドキュメント](https://flask.palletsprojects.com/)
- `ProjectProposal.md`: 詳細な機能仕様
- `.github/copilot-instructions.md`: AI開発者向けガイド
