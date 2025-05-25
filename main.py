import pygame
import pymunk
import pymunk.pygame_util

# 画面設定
WIDTH, HEIGHT = 400, 600
FPS = 60
BLOCK_SIZE = (60, 30)
DROP_INTERVAL_MS = 5000

# 初期化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stack Tower")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)  # ✅ デバッグ描画用フォント


# 物理空間
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 地面
floor = pymunk.Segment(space.static_body, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 5)
floor.friction = 1.0
space.add(floor)

# 現在操作中のブロック
current_block = None
last_drop_time = pygame.time.get_ticks()


# ブロック作成
def create_block(x_pos):
    mass = 1
    size = BLOCK_SIZE
    moment = pymunk.moment_for_box(mass, size)

    body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)  # 初期は手動移動
    body.position = (x_pos, 50)

    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.7
    space.add(body, shape)
    return body


# 最初のブロック生成
current_block = create_block(WIDTH // 2)


# 落下処理
def drop_block():
    global current_block, last_drop_time
    if current_block is None:
        return

    # 落下を開始（動的に変える）
    current_block.body_type = pymunk.Body.DYNAMIC
    current_block.velocity = (0, 1)  # ← 少しでも速度があると物理計算が始まる！
    current_block = create_block(WIDTH // 2)
    last_drop_time = pygame.time.get_ticks()

    # デバッグ文字描画
def draw_debug_text(text, pos):
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, pos)


# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and current_block:
            x = current_block.position.x
            if event.key == pygame.K_LEFT:
                current_block.position = (max(30, x - 20), current_block.position.y)
            elif event.key == pygame.K_RIGHT:
                current_block.position = (
                    min(WIDTH - 30, x + 20),
                    current_block.position.y,
                )

    # 5秒経過で自動落下
    now = pygame.time.get_ticks()
    if now - last_drop_time >= DROP_INTERVAL_MS:
        drop_block()

    screen.fill((240, 240, 240))
    space.step(1 / FPS)
    space.debug_draw(draw_options)

    # ✅ デバッグ表示（操作中ブロックのX位置）
    if current_block:
        draw_debug_text(f"x = {current_block.position.x:.1f}", (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
