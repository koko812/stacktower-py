# 🧱 Stack Tower

**物理演算でブロックを積み上げるタイムアタック型のミニゲーム！**

30秒間で、ランダムな形と角度を持つブロックをどれだけ高く積めるかを競います。

---

## 🎮 ゲームの特徴

* `pymunk` を使用したリアルな物理挙動
* ブロックはランダムな形（box / tall / tilted）と初期角度を持つ
* 落下は自動または `↓キー` による手動のどちらでも可能
* **高さスコアは接地済みブロックの最上端を基準に計算**
* 終了時に `Finished!` 表示と赤線で塔の頂点を明示
* 見た目と物理のズレを修正し、直感的なプレイ感に仕上げました

<a href="https://gyazo.com/28e922549f6e470a0623260330c6e9bf">
    <img src="https://i.gyazo.com/28e922549f6e470a0623260330c6e9bf.png" width="400" />
</a>

---

## 🕹️ 操作方法

| キー  | 動作               |
| --- | ---------------- |
| ←   | ブロックを左に移動        |
| →   | ブロックを右に移動        |
| ↓   | ブロックを即座に落下       |
| ESC | ゲーム終了（ウィンドウを閉じる） |

---

## ⏱️ ゲームルール

* 制限時間は30秒
* スコアは「接地済みブロックの最上端の高さ」
* 終了時に最終スコアが表示され、塔の高さに赤線が引かれます

---

## 🛠 技術スタック

* Python 3.12+
* [pygame](https://www.pygame.org/) 2.6+
* [pymunk](http://www.pymunk.org/)（物理エンジン）

---

## 🚀 実行方法

```bash
uv pip install -r requirements.txt
uv run main.py
```

---

## 📦 今後の展望

* スペースキーで再スタート機能
* 音やエフェクトの導入
* 強化学習環境としての抽象化（gym-like）
* 高さログやスコア履歴の保存

---

## 👀 プレイヤーの気づき

* 思ったより積むのが難しく、戦略と器用さが必要！
* 落とす「タイミング」もスコアに大きく影響する
* 見た目の整合性がゲーム体験に直結する（床の浮きなど）
* 強化学習で扱うには難易度が高い。前段階の環境が必要そうだと感じた。
