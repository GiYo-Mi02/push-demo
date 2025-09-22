import os
import sys
import random
import subprocess
from typing import Optional, List
import pygame

# Simple top-down racing game that opens a separate lyrics window on collision.
# Controls: Left/Right arrows or A/D to move. ESC to quit. R to restart after crash.

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
ROAD_MARGIN = 60  # left/right road margins
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 80
SPAWN_INTERVAL_MS = 900
ENEMY_SPEED_START = 4
ENEMY_SPEED_INC_EVERY = 10  # seconds
PLAYER_SPEED = 6
BG_COLOR = (30, 30, 30)
ROAD_COLOR = (50, 50, 50)
LANE_COLOR = (200, 200, 200)
PLAYER_COLOR = (60, 180, 75)
ENEMY_COLOR = (230, 41, 55)
TEXT_COLOR = (240, 240, 240)


def resource_path(*parts: str) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def open_with_default_app(path: str) -> bool:
    """Open a file with the OS default application. Returns True if launched."""
    try:
        if os.name == 'nt':
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
        return True
    except Exception as e:
        print(f"Failed to open file: {e}")
        return False

def find_video_in_assets() -> Optional[str]:
    """Find a video file in the assets folder. Prefer 'crash.mp4', else first supported video file."""
    assets_dir = resource_path('assets')
    supported = {'.mp4', '.mkv', '.avi', '.mov', '.webm'}
    preferred = os.path.join(assets_dir, 'crash.mp4')
    if os.path.exists(preferred):
        return preferred
    if os.path.isdir(assets_dir):
        for name in os.listdir(assets_dir):
            ext = os.path.splitext(name)[1].lower()
            if ext in supported:
                return os.path.join(assets_dir, name)
    return None


def draw_text(surface, text, size, x, y, color=TEXT_COLOR, center=True):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(render, rect)


def main():
    pygame.init()
    pygame.display.set_caption("Racing + Lyrics on Crash")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    road_left = ROAD_MARGIN
    road_right = SCREEN_WIDTH - ROAD_MARGIN

    player = pygame.Rect((SCREEN_WIDTH - PLAYER_WIDTH) // 2,
                         SCREEN_HEIGHT - PLAYER_HEIGHT - 20,
                         PLAYER_WIDTH, PLAYER_HEIGHT)

    enemies: List[pygame.Rect] = []
    enemy_speed = ENEMY_SPEED_START

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, SPAWN_INTERVAL_MS)

    score = 0.0
    elapsed_since_speedup = 0.0
    running = True
    game_over = False
    media_launched = False

    # Optional default media path (video). We auto-detect in assets.
    last_media_error: Optional[str] = None

    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_EVENT and not game_over:
                lane_width = (road_right - road_left - ENEMY_WIDTH)
                x = road_left + random.randint(0, max(0, lane_width))
                enemies.append(pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        if not game_over:
            # Movement
            dx = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += PLAYER_SPEED
            player.x += dx
            # Clamp within road
            player.x = max(road_left, min(player.x, road_right - player.width))

            # Update enemies
            for e in enemies:
                e.y += enemy_speed
            enemies = [e for e in enemies if e.top < SCREEN_HEIGHT + 10]

            # Collision detection
            hit = next((e for e in enemies if e.colliderect(player)), None)
            if hit is not None:
                game_over = True
                if not media_launched:
                    media_launched = True
                    video_path = find_video_in_assets()
                    if video_path and os.path.exists(video_path):
                        ok = open_with_default_app(video_path)
                        if not ok:
                            last_media_error = "Couldn't open video file."
                    else:
                        last_media_error = "No video found in assets (try assets/crash.mp4)."

            # Score and difficulty
            score += dt
            elapsed_since_speedup += dt
            if elapsed_since_speedup >= ENEMY_SPEED_INC_EVERY:
                enemy_speed += 0.5
                elapsed_since_speedup = 0.0
        else:
            # Allow restart
            if keys[pygame.K_r]:
                # Reset state
                player.topleft = ((SCREEN_WIDTH - PLAYER_WIDTH) // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 20)
                enemies.clear()
                enemy_speed = ENEMY_SPEED_START
                score = 0.0
                elapsed_since_speedup = 0.0
                game_over = False
                media_launched = False
                last_media_error = None

        # Drawing
        screen.fill(BG_COLOR)
        # Road
        pygame.draw.rect(screen, ROAD_COLOR, (road_left, 0, road_right - road_left, SCREEN_HEIGHT))
        # Lane markers
        for y in range(-40, SCREEN_HEIGHT, 80):
            pygame.draw.rect(screen, LANE_COLOR, (SCREEN_WIDTH // 2 - 5, y + int(pygame.time.get_ticks()/5) % 80, 10, 40))

        # Player and enemies
        pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=6)
        for e in enemies:
            pygame.draw.rect(screen, ENEMY_COLOR, e, border_radius=6)

        draw_text(screen, f"Score: {int(score)}", 24, 10, 10, center=False)

        if game_over:
            draw_text(screen, "CRASH!", 64, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)
            if last_media_error:
                draw_text(screen, last_media_error, 24, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)
            else:
                draw_text(screen, "Video should be playing (default player).", 24, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)
            draw_text(screen, "Press R to restart, ESC to quit", 24, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
