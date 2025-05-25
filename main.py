"""
Stack Tower v1.3.5 - 赤線をブロック最上端に合わせて表示
"""

import pygame
import pymunk
import random

# --- 設定 ---
WIDTH, HEIGHT = 400, 600
FPS = 60
DROP_INTERVAL_MS = 3000
NEW_BLOCK_DELAY_MS = 500
MOVE_STEP = 5
GAME_DURATION_MS = 30000  # 30秒

# --- 初期化 ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stack Tower v1.3.5")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
large_font = pygame.font.SysFont(None, 48)

space = pymunk.Space()
space.gravity = (0, 900)

floor = pymunk.Segment(space.static_body, (0, HEIGHT - 5), (WIDTH, HEIGHT - 5), 10)
floor.friction = 1.0
space.add(floor)

# --- 状態管理 ---
current_block = None
block_ready = True
scheduled_create_time = None
last_drop_time = pygame.time.get_ticks()
fallen_blocks = []
settled_blocks = []
start_time = pygame.time.get_ticks()
game_over = False

# --- 難易度係数管理 ---
difficulty_table = {"box": 1, "tall": 1.5, "tilted": 2}


# --- スコア計算 ---
def calculate_score():
    if not settled_blocks:
        return 0, HEIGHT
    min_top_y = HEIGHT
    for shape in settled_blocks:
        body = shape.body
        verts = shape.get_vertices()
        pts = [v.rotated(body.angle) + body.position for v in verts]
        top_y = min(p.y for p in pts)
        if top_y < min_top_y:
            min_top_y = top_y
    tower_height = HEIGHT - min_top_y
    return int(tower_height), int(min_top_y)


# --- ブロック生成 ---
def create_block(x_pos):
    mass = 1
    shape_type = random.choice(["box", "tall", "tilted"])
    size = (60, 30) if shape_type != "tall" else (40, 60)
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.KINEMATIC)
    body.position = (x_pos, 50)
    body.velocity = (0, 0)
    body.angle = random.uniform(-0.2, 0.2) if shape_type == "tilted" else 0
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.7
    shape.user_data = {"type": shape_type, "size": size, "angle": body.angle}
    space.add(body, shape)
    return body


# --- ブロック落下 ---
def drop_block():
    global current_block, block_ready, scheduled_create_time, last_drop_time
    if current_block is None:
        return
    shape_list = list(current_block.shapes)
    if not shape_list:
        return
    user_data = shape_list[0].user_data
    shape_type = user_data["type"]
    size = user_data["size"]
    angle = user_data.get("angle", 0)
    for s in current_block.shapes:
        space.remove(s)
    space.remove(current_block)
    mass = 1
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
    body.position = current_block.position
    body.angle = angle
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.7
    shape.user_data = {"type": shape_type, "size": size, "angle": angle}
    space.add(body, shape)
    fallen_blocks.append(shape)
    current_block = None
    block_ready = False
    scheduled_create_time = pygame.time.get_ticks() + NEW_BLOCK_DELAY_MS
    last_drop_time = pygame.time.get_ticks()


# --- 描画関数 ---
def draw_block(shape, color):
    body = shape.body
    verts = shape.get_vertices()
    pts = [v.rotated(body.angle) + body.position for v in verts]
    pts = [(int(p.x), int(p.y)) for p in pts]
    pygame.draw.polygon(screen, color, pts)


def draw_debug_text(text, pos, font_obj=font):
    img = font_obj.render(text, True, (0, 0, 0))
    screen.blit(img, pos)


# --- 初期ブロック生成 ---
current_block = create_block(WIDTH // 2)

# --- メインループ ---
pygame.draw.rect(
    screen, (100, 100, 100), (0, HEIGHT - 20, WIDTH, 20)
)  # 床描画（濃いグレーで明確に）
running = True
while running:
    now = pygame.time.get_ticks()
    elapsed = now - start_time
    if elapsed >= GAME_DURATION_MS:
        game_over = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_DOWN:
                drop_block()

    if not game_over:
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
        if block_ready and now - last_drop_time >= DROP_INTERVAL_MS:
            drop_block()
        if not block_ready and scheduled_create_time and now >= scheduled_create_time:
            current_block = create_block(WIDTH // 2)
            block_ready = True

    screen.fill((240, 240, 240))
    pygame.draw.rect(screen, (160, 160, 160), (0, HEIGHT - 20, WIDTH, 20))  # 床描画
    space.step(1 / FPS)

    for shape in fallen_blocks:
        draw_block(shape, (70, 130, 180))
        if shape not in settled_blocks and abs(shape.body.velocity.y) < 1.0:
            settled_blocks.append(shape)

    if current_block:
        for shape in current_block.shapes:
            draw_block(shape, (30, 180, 90))

    score, top_y = calculate_score()
    draw_debug_text(
        f"x = {current_block.position.x:.1f}" if current_block else "x = ...", (10, 10)
    )
    draw_debug_text(f"Score: {score}", (10, 30))
    draw_debug_text(
        f"Time Left: {max(0, (GAME_DURATION_MS - elapsed) // 1000)}s", (10, 50)
    )

    if game_over:
        draw_debug_text("Finished!", (WIDTH // 2 - 80, HEIGHT // 2 - 40), large_font)
        draw_debug_text(f"Final Score: {score}", (WIDTH // 2 - 90, HEIGHT // 2 + 10))
        pygame.draw.line(screen, (255, 0, 0), (0, top_y), (WIDTH, top_y), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
