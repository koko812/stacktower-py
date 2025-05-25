# 📘 LEARNED.md — Stack Tower 開発ログと学習メモ

このドキュメントは、`stacktower-py` の開発を進める中で得た知見や理解を時系列・構造的にまとめたものです。

---

## ✅ Initialization & Display（初期化と画面表示）

* `pygame.init()` は各種モジュール（表示・音声など）をまとめて初期化する。忘れると `pygame.error: video system not initialized` が起こる可能性がある。
* `pygame.display.set_mode()` はウィンドウサイズやフラグを指定できる。例えば `RESIZABLE`（サイズ変更可）、`FULLSCREEN`、`NOFRAME`（枠なし）などがある。
* `pygame.time.Clock()` によってフレームレート管理が可能となり、`clock.tick(FPS)` で 1 秒あたりの最大フレーム数を制限できる。

---

## ✅ Space and Gravity（物理空間と重力）

* `pymunk.Space()` は物理世界を表す中心オブジェクト。
* `space.gravity = (0, 900)` によって y 軸下方向に加速度がかかる（単位は pixel/s^2）。
* `space.step(dt)` によって世界が dt 秒だけ進行する。

---

## ✅ Static vs Dynamic Bodies（固定物体と可動物体）

* **地面**は `pymunk.Segment(...)` を `space.static_body` に紐づけて作成。動かず、摩擦や衝突の判定には使われる。
* **ブロック**は `pymunk.Body(mass, moment)` で生成され、質量と回転しやすさ（moment）を持つ。
* `space.add()` によって Space に存在させなければ動作しない。

---

## ✅ Shapes and Positioning（形状と位置指定）

* ブロックの形状には `pymunk.Poly.create_box(...)` を使用。これは `Poly` のショートカットで、中心を原点にした矩形を生成する。
* `body.position = (x, y)` によって物体の重心位置が決まる。
* `Segment`, `Circle`, 任意の `Poly` など、他の形状も存在する。

---

## ✅ Game Loop（ゲームループ）

```python
while running:
    pygame.event.get()     # 入力イベント処理
    screen.fill(...)       # 背景をリセット
    space.step(1/FPS)      # 物理演算を1フレーム進行
    space.debug_draw(...)  # pymunkによる描画
    pygame.display.flip()  # 表示の更新
    clock.tick(FPS)        # フレームレートの調整
```

* `screen.fill()` は前フレームの残像を消すために必要。
* `space.step()` の dt と `clock.tick(FPS)` の FPS を一致させることで、安定した挙動が得られる。
* `flip()` は画面全体を更新し、`tick()` によって無限ループの暴走を防ぐ。

---

## ✅ 時間ステップ設計と物理安定性

* 固定ステップ（`dt = 1 / FPS`）は再現性・安定性があり、教育・強化学習にも向いている。
* 可変ステップ（`dt = clock.tick(...) / 1000`）は実時間ベースで柔軟だが、不安定になりやすく、再現性が低下する。
* `pymunk` の推奨は「固定ステップ + 安定フレームレート」である。

---

## ✅ その他補足

* `debug_draw()` は物理世界の可視化に便利だが、見た目のカスタマイズには不向き。
* UI（スコアやボタンなど）は別レイヤーで描画すれば問題なし。
* 慣れてきたら `debug_draw` をやめて、自前で `pygame.draw.rect()` などを使って描画する方向に進むと良い。

---

> 📌 まとめ：**「Body（状態） + Shape（形） + Space（世界）」で構成される物理世界**を、clock と loop で回していくという設計が pymunk の基本構造。
