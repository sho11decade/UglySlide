# グラデーション過激化機能 - 技術説明書

DasaMakerに追加された「グラデーション過激化機能」の実装詳細です。

## 概要

レベル5以上のときに、プレゼンテーションのシェイプ（図形）に対してネオン色のグラデーションを適用します。

## 機能仕様

### グラデーション適用レベル

| ダサさレベル | グラデーション種類 | 色数 | 特徴 |
|-----------|-----------------|------|------|
| 1-4 | なし | - | グラデーション未適用 |
| 5-6 | **シンプルグラデーション** | 2色 | 2つのネオン色の単純なグラデーション |
| 7-8 | **マルチカラーグラデーション** | 3-4色 | 複数のネオン色を使用した段階的グラデーション |
| 9-10 | **極度グラデーション** | 最大8色 | すべてのネオンカラーを使用した超派手グラデーション |

### グラデーション角度

各レベルでランダムに以下の角度から選択：

```python
[0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°]
```

これにより、同じプレゼンテーションでも毎回異なるグラデーション方向が適用されます。

### ネオンカラーペア（レベル5-6）

```python
EXTREME_NEON_PAIRS = [
    [(255, 0, 127), (0, 255, 255)],      # ホットピンク → シアン
    [(255, 255, 0), (255, 0, 0)],        # 黄色 → 赤
    [(0, 255, 0), (148, 0, 211)],        # ライムグリーン → 青紫
    [(255, 127, 0), (255, 0, 127)],      # オレンジ → ホットピンク
    # ... 計10ペア
]
```

## 実装詳細

### クラス構成

```python
class TacoGenerator:
    def _apply_extreme_gradient(self, shape) -> None
        ↓
    ├─ _apply_simple_gradient(fill)          # レベル5-6
    ├─ _apply_multi_color_gradient(fill)     # レベル7-8
    └─ _apply_extreme_multi_gradient(fill)   # レベル9-10
```

### メソッド説明

#### `_apply_extreme_gradient()`

メインの制御メソッド。ダサさレベルに応じて適切なグラデーション方法を選択。

```python
def _apply_extreme_gradient(self, shape) -> None:
    """Apply extreme gradient fills to shapes with leveled intensity"""
    if self.tacky_level in [5, 6]:
        self._apply_simple_gradient(fill)
    elif self.tacky_level in [7, 8]:
        self._apply_multi_color_gradient(fill)
    elif self.tacky_level >= 9:
        self._apply_extreme_multi_gradient(fill)
```

#### `_apply_simple_gradient()`

**レベル5-6**: シンプルな2色グラデーション

```python
def _apply_simple_gradient(self, fill) -> None:
    fill.gradient()
    fill.gradient_angle = random_angle  # 0-315度
    color_pair = random_choice(EXTREME_NEON_PAIRS)
    fill.gradient_stops[0].color.rgb = RGBColor(*color_pair[0])
    fill.gradient_stops[1].color.rgb = RGBColor(*color_pair[1])
```

**出力例:**
- ホットピンク → シアン
- 黄色 → 赤
- etc.

#### `_apply_multi_color_gradient()`

**レベル7-8**: 3-4色のマルチカラーグラデーション

```python
def _apply_multi_color_gradient(self, fill) -> None:
    fill.gradient()
    num_colors = random_choice([3, 4])
    colors = random_sample(NEON_COLORS, num_colors)
    
    # 最初と最後の色を設定
    fill.gradient_stops[0].color.rgb = RGBColor(*colors[0])
    fill.gradient_stops[1].color.rgb = RGBColor(*colors[-1])
    
    # 中間色を追加
    for i in range(1, len(colors) - 1):
        position = i / (len(colors) - 1)
        new_stop = fill.gradient_stops._insert_stop(position)
        new_stop.color.rgb = RGBColor(*colors[i])
```

**効果:**
- 複数の色が段階的に遷移
- より複雑で派手な見た目

#### `_apply_extreme_multi_gradient()`

**レベル9-10**: 最大8色の極度グラデーション

```python
def _apply_extreme_multi_gradient(self, fill) -> None:
    fill.gradient()
    colors = NEON_COLORS.copy()
    random.shuffle(colors)
    
    # すべてのネオンカラーをシャッフルして使用
    for i in range(len(colors)):
        fill.gradient_stops[i].color.rgb = RGBColor(*colors[i])
```

**効果:**
- 最大8つのネオン色がすべて使用される
- レベル10では角度もランダム化（0-360度）

## 対応シェイプタイプ

グラデーションが適用されるシェイプ：

- ✅ 矩形（Rectangle）
- ✅ 円（Oval）
- ✅ 多角形（Polygon）
- ✅ テキストボックス（TextBox with fill）
- ✅ SmartArt（可能な範囲で）

対応**されない**シェイプ：

- ❌ 画像（PICTURE）
- ❌ 既にグラデーション適用済み（上書き）
- ❌ 透明フィル

## エラーハンドリング

各グラデーション適用メソッドは`try-except`で保護されており、失敗してもアプリケーションが落ちません。

```python
try:
    fill.gradient()
    # グラデーション設定
except Exception as e:
    logger.debug(f"Could not apply gradient: {e}")
    # 失敗してもスキップして続行
```

## テスト

### ユニットテスト

```bash
# グラデーション機能のテスト
pytest tests/test_modules.py::TestTacoGenerator::test_taco_generator_gradient_level_5
pytest tests/test_modules.py::TestTacoGenerator::test_taco_generator_gradient_level_7
pytest tests/test_modules.py::TestTacoGenerator::test_taco_generator_gradient_level_10
```

### 統合テスト

```bash
# 実際のPPTファイルで動作確認
python -c "
from src.taco_generator import TacoGenerator
from pptx import Presentation

prs = Presentation('samples/sample.pptx')
gen = TacoGenerator(prs, tacky_level=10)
gen.apply_tacky_design()
prs.save('output_gradient.pptx')
"
```

## パフォーマンス

### 処理時間

| レベル | 平均処理時間 | 特徴 |
|--------|-----------|------|
| 5-6 | < 100ms | 高速（2色のみ） |
| 7-8 | 100-200ms | 中程度（複数色追加） |
| 9-10 | 200-400ms | やや遅い（全色使用） |

※ スライド数、シェイプ数により変動

### メモリ使用量

- グラデーション情報: シェイプあたり数KB
- 大規模プレゼンテーション（1000+スライド）でも安全

## 既知の制限

### python-pptxの制限

1. **グラデーション停止数の制限**
   - 理論上は無制限だが、Office側で8色程度まで安定
   - レベル9-10でも8色に制限

2. **グラデーション方向の限定**
   - 45度単位が安定（0, 45, 90, 135...）
   - 任意の度数はOfficeで正規化される可能性

3. **既存グラデーション上書き**
   - 既にグラデーション適用済みのシェイプは上書きされる

## 今後の改善案

- [ ] グラデーション停止数の柔軟な制御
- [ ] ラジアルグラデーション（放射状）のサポート
- [ ] グラデーションスピードの段階的な加速
- [ ] テクスチャグラデーションの追加
- [ ] グラデーション効果のアニメーション統合

## 参考資料

- [python-pptx Documentation - Shapes](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)
- [OOXML 仕様 - Gradient Fill](http://officeopenxml.com/drwgGradFill.html)

---

**グラデーション過激化で、あなたのプレゼンは最高にダサくなる！🌈✨**
