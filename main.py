import pygame
import pymunk
import pymunk.pygame_util

# 初期設定
WIDTH, HEIGHT = 400, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stack Tower")
clock = pygame.time.Clock()

# 物理空間のセットアップ
space = pymunk.Space()
space.gravity = (0, 900)  # 下向き重力

# デバッグ描画設定
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 地面（静的セグメント）
floor = pymunk.Segment(space.static_body, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 5)
floor.friction = 1.0
space.add(floor)


# ブロックを生成する関数
def create_block():
    mass = 1
    size = (60, 30)
    moment = pymunk.moment_for_box(mass, size)

    body = pymunk.Body(mass, moment)
    body.position = (WIDTH // 2, 50)

    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.7

    space.add(body, shape)
    return body


block_body = create_block()

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 描画クリア
    screen.fill((240, 240, 240))

    # 物理演算ステップ
    space.step(1 / FPS)

    # pymunk デバッグ描画
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
