"""
Juego integrado: control de nave, recolección de objetos y evitar obstáculos. (FINAL)
Cumple los requisitos del Mini-proyecto.
¡Imagen de nave personalizada!
"""

import sys
import math
import random
from pathlib import Path
import pygame

# Configuración y Colores
WIDTH, HEIGHT = 900, 650
FPS = 55

# Nave del jugador
SHIP_SIZE = (64, 64)  # AJUSTADO para la nueva imagen de nave (64x64)
SHIP_IMAGE_NAME = "ship.png"  # <--- ¡CAMBIADO AQUÍ! Nombre de tu imagen
SHIP_SPEED = 5
# Este color ahora solo se usa si la imagen no se carga
SHIP_COLOR = (255, 255, 0)

# Objetos a recoger (MONEDAS / Puntos)
COIN_RADIUS = 10
COIN_COLOR = (0, 255, 0)  # Color verde
INITIAL_COINS = 7

# Obstáculos (MINAS)
MINE_RADIUS = 15
MINE_COLOR = (255, 50, 0)  # Color rojo brillante
MINE_SPEED = 3
INITIAL_MINES = 4

BACKGROUND_COLOR = (10, 30, 10)

pygame.init()
pygame.joystick.init()

# --- Funciones de Utilidad (load_ship_image modificada) ---


def load_ship_image(image_name: str, size: tuple) -> pygame.Surface:
    """Carga la imagen o usa una nave triangular amarilla por defecto."""
    script_dir = Path(__file__).resolve().parent
    image_path = script_dir / image_name

    def _fallback_yellow_ship(sz: tuple) -> pygame.Surface:
        # Esta es la nave por defecto si la imagen no se encuentra
        surf = pygame.Surface(sz, pygame.SRCALPHA)
        w, h = sz
        points = [
            (w // 2, h),
            (w, 0),
            (w // 2, int(h * 0.4)),
            (0, 0),
        ]
        # Usa SHIP_COLOR (amarillo)
        pygame.draw.polygon(surf, SHIP_COLOR, points)
        pygame.draw.polygon(surf, (200, 200, 50), points, 2)
        return surf

    if image_path.exists():
        try:
            img = pygame.image.load(str(image_path)).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception as e:
            print(
                f"Error cargando imagen {image_path}: {e} — usando nave por defecto.")
            return _fallback_yellow_ship(size)
    else:
        print(
            f"Imagen '{image_name}' no encontrada — usando nave por defecto.")
        return _fallback_yellow_ship(size)

# Resto de funciones (generate_coin, generate_mine, rotate_image, etc.) son las mismas


def generate_coin() -> dict:
    """Genera un objeto a recoger (moneda) en posición aleatoria."""
    return {
        'x': random.randint(COIN_RADIUS + 20, WIDTH - COIN_RADIUS - 20),
        'y': random.randint(COIN_RADIUS + 20, HEIGHT - COIN_RADIUS - 20),
    }


def generate_mine() -> dict:
    """Genera un obstáculo (mina) con movimiento aleatorio."""
    return {
        'x': float(random.randint(MINE_RADIUS + 50, WIDTH - MINE_RADIUS - 50)),
        'y': float(random.randint(MINE_RADIUS + 50, HEIGHT // 3)),
        'vx': random.choice([-MINE_SPEED, MINE_SPEED]),
        'vy': random.uniform(-1, 1) * MINE_SPEED * 0.7,
    }


def rotate_image(image: pygame.Surface, angle: float) -> pygame.Surface:
    return pygame.transform.rotate(image, -angle)


def normalize_angle_diff(current: float, target: float) -> float:
    diff = target - current
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff


def check_collision_rect_circle(rect_pos: tuple, rect_size: tuple, circle_pos: tuple, circle_radius: float) -> bool:
    rect = pygame.Rect(rect_pos[0] - rect_size[0] // 2,
                       rect_pos[1] - rect_size[1] // 2, rect_size[0], rect_size[1])
    circle_center = circle_pos
    closest_x = max(rect.left, min(circle_center[0], rect.right))
    closest_y = max(rect.top, min(circle_center[1], rect.bottom))
    dx = circle_center[0] - closest_x
    dy = circle_center[1] - closest_y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    return distance < circle_radius


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Juego Integrado - Mini-proyecto")
    clock = pygame.time.Clock()

    # <--- ¡LLAMADA A load_ship_image MODIFICADA! --->
    ship_original = load_ship_image(SHIP_IMAGE_NAME, SHIP_SIZE)

    # Estado del juego
    ship_x = WIDTH // 2
    ship_y = HEIGHT // 2
    ship_angle = 0.0
    score = 0
    game_over = False

    # Objetos y Obstáculos
    coins = [generate_coin() for _ in range(INITIAL_COINS)]
    mines = [generate_mine() for _ in range(INITIAL_MINES)]

    # Joystick
    joysticks = pygame.joystick.get_count()
    joystick = pygame.joystick.Joystick(0) if joysticks > 0 else None

    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            # Input: Teclado
            keys = pygame.key.get_pressed()
            move_x = 0
            move_y = 0

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                move_x -= SHIP_SPEED
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                move_x += SHIP_SPEED
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                move_y -= SHIP_SPEED
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                move_y += SHIP_SPEED

            # Tecla shift para acelerar
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                move_x *= 1.5
                move_y *= 1.5

            # Input: Joystick (sticks analógicos)
            if joystick:
                try:
                    lx = joystick.get_axis(0)
                    ly = joystick.get_axis(1)
                    if abs(lx) > 0.2:
                        move_x += int(lx * SHIP_SPEED)
                    if abs(ly) > 0.2:
                        move_y += int(ly * SHIP_SPEED)
                except (IndexError, RuntimeError):
                    pass
            # Input: Joystick RT para acelerar
            if joystick:
                try:
                    rt = joystick.get_axis(5)
                    if rt > 0.5:
                        move_x *= 1.5
                        move_y *= 1.5
                except (IndexError, RuntimeError):
                    pass

            # Aplicar movimiento
            ship_x += move_x
            ship_y += move_y

            # Limitar en pantalla
            ship_x = max(SHIP_SIZE[0] // 2,
                         min(ship_x, WIDTH - SHIP_SIZE[0] // 2))
            ship_y = max(SHIP_SIZE[1] // 2,
                         min(ship_y, HEIGHT - SHIP_SIZE[1] // 2))

            # Rotar hacia la dirección de movimiento
            if move_x != 0 or move_y != 0:
                angle_rad = math.atan2(move_y, move_x)
                target_angle = math.degrees(angle_rad) - 90
                angle_diff = normalize_angle_diff(ship_angle, target_angle)
                max_rotate = 5
                if abs(angle_diff) < max_rotate:
                    ship_angle = target_angle
                else:
                    ship_angle += max_rotate if angle_diff > 0 else -max_rotate

            # Actualizar minas
            for mine in mines:
                mine['x'] += mine['vx']
                mine['y'] += mine['vy']

                # Rebotar en bordes
                if mine['x'] - MINE_RADIUS < 0 or mine['x'] + MINE_RADIUS > WIDTH:
                    mine['vx'] *= -1
                if mine['y'] - MINE_RADIUS < 0 or mine['y'] + MINE_RADIUS > HEIGHT:
                    mine['vy'] *= -1

                mine['x'] = max(MINE_RADIUS, min(
                    mine['x'], WIDTH - MINE_RADIUS))
                mine['y'] = max(MINE_RADIUS, min(
                    mine['y'], HEIGHT - MINE_RADIUS))

            # Verificar colisión con monedas
            coins_to_remove = []
            for i, coin in enumerate(coins):
                if check_collision_rect_circle((ship_x, ship_y), SHIP_SIZE, (coin['x'], coin['y']), COIN_RADIUS):
                    score += 5
                    coins_to_remove.append(i)

            for i in reversed(coins_to_remove):
                coins.pop(i)
                coins.append(generate_coin())

            # Verificar colisión con minas (game over)
            for mine in mines:
                if check_collision_rect_circle((ship_x, ship_y), SHIP_SIZE, (mine['x'], mine['y']), MINE_RADIUS):
                    game_over = True
                    print(f"¡Explosión con mina! Score final: {score}")

        # Dibujado
        screen.fill(BACKGROUND_COLOR)

        if not game_over:
            # Dibujar nave (ahora usa la imagen cargada)
            ship_rotated = rotate_image(ship_original, ship_angle)
            rect = ship_rotated.get_rect(center=(int(ship_x), int(ship_y)))
            screen.blit(ship_rotated, rect)

            # Dibujar monedas
            for coin in coins:
                pygame.draw.circle(screen, COIN_COLOR, (int(
                    coin['x']), int(coin['y'])), COIN_RADIUS)
                pygame.draw.circle(screen, (50, 200, 50), (int(
                    coin['x']), int(coin['y'])), COIN_RADIUS, 1)

            # Dibujar minas
            for mine in mines:
                pygame.draw.circle(screen, MINE_COLOR, (int(
                    mine['x']), int(mine['y'])), MINE_RADIUS)
                pygame.draw.circle(screen, (200, 50, 0), (int(
                    mine['x']), int(mine['y'])), MINE_RADIUS, 2)
        else:
            # Pantalla de game over
            font_large = pygame.font.Font(None, 70)
            font_small = pygame.font.Font(None, 40)

            text_gameover = font_large.render(
                "DESTRUIDO", True, (255, 100, 100))
            text_score = font_small.render(
                f"Puntuación Final: {score}", True, (200, 200, 200))
            text_restart = font_small.render(
                "Presiona R para reiniciar", True, (150, 150, 150))

            screen.blit(text_gameover, (WIDTH // 2 -
                        text_gameover.get_width() // 2, 150))
            screen.blit(text_score, (WIDTH // 2 -
                        text_score.get_width() // 2, 280))
            screen.blit(text_restart, (WIDTH // 2 -
                        text_restart.get_width() // 2, 380))

            # Reiniciar con R o Start
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_over = False
                score = 0
                ship_x = WIDTH // 2
                ship_y = HEIGHT // 2
                ship_angle = 0.0
                coins = [generate_coin() for _ in range(INITIAL_COINS)]
                mines = [generate_mine() for _ in range(INITIAL_MINES)]

            if joystick:
                try:
                    if joystick.get_button(7):
                        game_over = False
                        score = 0
                        ship_x = WIDTH // 2
                        ship_y = HEIGHT // 2
                        ship_angle = 0.0
                        coins = [generate_coin() for _ in range(INITIAL_COINS)]
                        mines = [generate_mine() for _ in range(INITIAL_MINES)]
                except (IndexError, RuntimeError):
                    pass

        # Mostrar score en pantalla (cumple requisito de contador de puntos)
        if not game_over:
            font = pygame.font.Font(None, 36)
            score_text = font.render(
                f"Puntuación: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Información en pantalla
            font_small = pygame.font.Font(None, 20)
            info_lines = [
                "WASD/Flechas: Mover nave",
                "Shift/RT: Propulsión",
                "Verde: Recoger (+5)",
                "Rojo: ¡Peligro!",
            ]
            for i, line in enumerate(info_lines):
                info_text = font_small.render(line, True, (150, 200, 150))
                screen.blit(info_text, (10, HEIGHT - 90 + i * 20))

        # Aumentar velocidad de minas con el score
        for mine in mines:
            speed_increase = score // 25
            mine['vx'] = (MINE_SPEED + speed_increase) * \
                (1 if mine['vx'] > 0 else -1)
            mine['vy'] = (MINE_SPEED * 0.7 + speed_increase *
                          0.7) * (1 if mine['vy'] > 0 else -1)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
