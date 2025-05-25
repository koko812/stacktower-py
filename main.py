import pygame
import pymunk

# --- 設定 ---
WIDTH, HEIGHT = 400, 600
FPS = 60
BLOCK_SIZE = (60, 30)
DROP_INTERVAL_MS = 3000
NEW_BLOCK_DELAY_MS = 500
MOVE_STEP = 5  # ← お好みで調整可


# --- 初期化 ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stack Tower")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

space = pymunk.Space()
space.gravity = (0, 900)

floor = pymunk.Segment(space.static_body, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 5)
floor.friction = 1.0
space.add(floor)

# --- ゲーム状態 ---
current_block = None
last_drop_time = pygame.time.get_ticks()
block_ready = True
scheduled_create_time = None
fallen_blocks = []


# --- ブロック生成 ---
def create_block(x_pos):
    mass = 1
    moment = pymunk.moment_for_box(mass, BLOCK_SIZE)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
    body.position = (x_pos, 50)
    body.velocity = (0, 0)
    shape = pymunk.Poly.create_box(body, BLOCK_SIZE)
    shape.friction = 0.7
    space.add(body, shape)
    return body


# --- ブロック落下 ---
def drop_block():
    global current_block, last_drop_time, block_ready, scheduled_create_time
    if current_block is None:
        return

    # 操作中のブロックを削除（Shapeだけ）
    for s in current_block.shapes:
        space.remove(s)
    space.remove(current_block)

    # DYNAMICで作り直して追加
    mass = 1
    moment = pymunk.moment_for_box(mass, BLOCK_SIZE)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = current_block.position
    shape = pymunk.Poly.create_box(body, BLOCK_SIZE)
    shape.friction = 0.7
    space.add(body, shape)
    fallen_blocks.append(shape)

    current_block = None
    block_ready = False
    scheduled_create_time = pygame.time.get_ticks() + NEW_BLOCK_DELAY_MS
    last_drop_time = pygame.time.get_ticks()


# --- 自前描画関数 ---
def draw_block(shape, color):
    body = shape.body
    verts = shape.get_vertices()
    pts = [v.rotated(body.angle) + body.position for v in verts]
    pts = [(int(p.x), int(p.y)) for p in pts]
    pygame.draw.polygon(screen, color, pts)


def draw_debug_text(text, pos):
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, pos)


# --- 初回ブロック生成 ---
current_block = create_block(WIDTH // 2)

# --- メインループ ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # キー押しっぱなし対応（← →）

    keys = pygame.key.get_pressed()
    if current_block:
        x = current_block.position.x
        if keys[pygame.K_LEFT]:
            current_block.position = (
                max(30, x - MOVE_STEP),
                current_block.position.y,
            )
        if keys[pygame.K_RIGHT]:
            current_block.position = (
                min(WIDTH - 30, x + MOVE_STEP),
                current_block.position.y,
            )

    # 落下タイミングチェック
    now = pygame.time.get_ticks()
    if block_ready and now - last_drop_time >= DROP_INTERVAL_MS:
        drop_block()

    # 新ブロック生成の遅延処理
    if not block_ready and scheduled_create_time and now >= scheduled_create_time:
        current_block = create_block(WIDTH // 2)
        block_ready = True

    screen.fill((240, 240, 240))
    space.step(1 / FPS)

    # 描画：落下済ブロック
    for shape in fallen_blocks:
        draw_block(shape, (70, 130, 180))  # 青っぽい

    # 描画：操作中ブロック
    if current_block:
        for shape in current_block.shapes:
            draw_block(shape, (30, 180, 90))  # 緑

    draw_debug_text(
        f"x = {current_block.position.x:.1f}" if current_block else "x = ...", (10, 10)
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
