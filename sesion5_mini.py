"""
Nave que rota hacia el ratón/joystick y se mueve hacia adelante.
Restaurada a la configuración y colores más simples del original.

Controles:
  - Ratón: la nave rota hacia la posición del ratón
  - Joystick analógico derecho: rota hacia la dirección del joystick (si está disponible)
  - Tecla W / Botón RB (joystick): mueve la nave hacia adelante
  - ESC: salir
"""

import sys
import math
from pathlib import Path
import pygame

# Configuración RESTAURADA
WIDTH, HEIGHT = 800, 600
FPS = 60
SHIP_SIZE = (64, 64)  # tamaño para escalar la imagen
SHIP_SPEED = 5        # Velocidad restaurada a 5
ROTATION_SPEED = 5    # Velocidad de rotación restaurada a 5

pygame.init()
pygame.joystick.init()

# Función restaurada para dibujar la nave por defecto en AZUL


def create_default_ship(size: int = 64) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    w, h = size, size
    # Dibuja un triángulo que apunta hacia abajo
    points = [
        (w // 2, 0),        # punta
        (w, h),             # abajo derecha
        (w // 2, h * 0.6),  # centro trasero
        (0, h),             # abajo izquierda
    ]
    pygame.draw.polygon(surf, (100, 200, 255), points)  # Color azul claro
    pygame.draw.polygon(surf, (50, 150, 255), points, 2)
    return surf

# Funciones de carga, rotación y ángulos (sin cambios)


def load_or_create_ship(image_name: str, size: tuple) -> pygame.Surface:
    script_dir = Path(__file__).resolve().parent
    image_path = script_dir / image_name

    if image_path.exists():
        print(f"Cargada imagen: {image_path}")
        img = pygame.image.load(str(image_path)).convert_alpha()
    else:
        print(f"Imagen no encontrada ({image_path}). Usando nave por defecto.")
        img = create_default_ship(size[0])

    return pygame.transform.scale(img, size)


def rotate_image(image: pygame.Surface, angle: float) -> pygame.Surface:
    return pygame.transform.rotate(image, -angle)


def get_direction_to_target(ship_pos: tuple, target_pos: tuple) -> float:
    dx = target_pos[0] - ship_pos[0]
    dy = target_pos[1] - ship_pos[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    return angle_deg - 90


def normalize_angle_diff(current: float, target: float) -> float:
    diff = target - current
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nave - Ratón/Joystick (SIMPLE)")
    clock = pygame.time.Clock()

    ship_original = load_or_create_ship("nave.png", SHIP_SIZE)

    ship_x = WIDTH // 2
    ship_y = HEIGHT // 2
    ship_angle = 0.0
    ship_vel_x = 0.0
    ship_vel_y = 0.0

    joysticks = pygame.joystick.get_count()
    joystick = pygame.joystick.Joystick(0) if joysticks > 0 else None
    if joystick:
        print(f"Joystick detectado: {joystick.get_name()}")

    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Rotación hacia el ratón
        mouse_pos = pygame.mouse.get_pos()
        target_angle = get_direction_to_target((ship_x, ship_y), mouse_pos)

        angle_diff = normalize_angle_diff(ship_angle, target_angle)
        max_rotate = ROTATION_SPEED
        if abs(angle_diff) < max_rotate:
            ship_angle = target_angle
        else:
            ship_angle += max_rotate if angle_diff > 0 else -max_rotate

        # Rotación por Joystick
        if joystick:
            try:
                rx = joystick.get_axis(2)
                ry = joystick.get_axis(3)

                if abs(rx) > 0.1 or abs(ry) > 0.1:
                    joystick_angle = math.degrees(math.atan2(ry, rx)) - 90
                    angle_diff = normalize_angle_diff(
                        ship_angle, joystick_angle)
                    # ROTATION_SPEED * 2 es un pequeño feature que dejé para dar más control al joystick
                    max_rotate = ROTATION_SPEED * 2
                    if abs(angle_diff) < max_rotate:
                        ship_angle = joystick_angle
                    else:
                        ship_angle += max_rotate if angle_diff > 0 else -max_rotate
            except (IndexError, RuntimeError):
                pass

        # Movimiento (Tecla W o Botón)
        keys = pygame.key.get_pressed()
        move_forward = keys[pygame.K_w]

        if joystick:
            try:
                if joystick.get_button(5):
                    move_forward = True
            except (IndexError, RuntimeError):
                pass

        # Aplicar movimiento
        if move_forward:
            angle_rad = math.radians(ship_angle + 90)
            ship_vel_x = SHIP_SPEED * math.cos(angle_rad)
            ship_vel_y = SHIP_SPEED * math.sin(angle_rad)
        else:
            # Fricción restaurada a 0.95
            ship_vel_x *= 0.95
            ship_vel_y *= 0.95

        # Actualizar posición
        ship_x += ship_vel_x
        ship_y += ship_vel_y

        # Mantener en pantalla (envolvimiento opcional)
        if ship_x < -50:
            ship_x = WIDTH + 50
        elif ship_x > WIDTH + 50:
            ship_x = -50

        if ship_y < -50:
            ship_y = HEIGHT + 50
        elif ship_y > HEIGHT + 50:
            ship_y = -50

        # Dibujado
        screen.fill((20, 20, 40))  # Fondo restaurado a azul muy oscuro

        ship_rotated = rotate_image(ship_original, ship_angle)
        rect = ship_rotated.get_rect(center=(int(ship_x), int(ship_y)))
        screen.blit(ship_rotated, rect)

        # Dibujar línea hacia ratón (debug)
        pygame.draw.line(screen, (200, 200, 200),
                         (ship_x, ship_y), mouse_pos, 1)

        # Info en pantalla
        font = pygame.font.Font(None, 24)
        text_lines = [
            f"Ángulo: {ship_angle:.1f}°",
            f"Pos: ({ship_x:.0f}, {ship_y:.0f})",
            "W para mover | Ratón para rotar",
        ]
        for i, line in enumerate(text_lines):
            surf = font.render(line, True, (255, 255, 255))
            screen.blit(surf, (10, 10 + i * 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
