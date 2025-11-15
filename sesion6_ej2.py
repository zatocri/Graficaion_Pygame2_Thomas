"""
Juego simple: recoger círculos aleatorios. (Ajustado para cumplir requisitos)

Controles:
 - Flechas o WASD: mover rectángulo jugador
 - Esc: salir

El jugador (rectángulo) debe recoger círculos que aparecen en pantalla.
"""

import sys
import random
import pygame
from pygame import Rect

# --- Configuración y Colores (Ajustados de _mod) ---
WIDTH, HEIGHT = 900, 500  # Nuevo tamaño de ventana
FPS = 50

# Jugador (RECTÁNGULO - Requerimiento cumplido)
PLAYER_SIZE = (50, 40)  # ancho, alto (Tamaño del original)
PLAYER_COLOR = (50, 200, 150)  # Color del _mod
PLAYER_SPEED = 7  # Velocidad del _mod

# Pickup (CÍRCULO - Requerimiento cumplido)
PICKUP_RADIUS = 15  # Radio ligeramente mayor
PICKUP_COLOR = (255, 50, 200)  # Color magenta del _mod

BACKGROUND_COLOR = (50, 0, 50)  # Fondo oscuro del _mod
TEXT_COLOR = (255, 255, 0)  # Texto amarillo del _mod


def spawn_pickup_center():
    """Genera la posición central (x, y) de un nuevo círculo."""
    x = random.randint(PICKUP_RADIUS, WIDTH - PICKUP_RADIUS)
    y = random.randint(PICKUP_RADIUS, HEIGHT - PICKUP_RADIUS)
    return (x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Recolecta Círculos (Final)")
    clock = pygame.time.Clock()

    # Jugador (Rectángulo)
    player_rect = Rect((WIDTH // 2, HEIGHT // 2), PLAYER_SIZE)

    # Pickup inicial (Centro del Círculo)
    pickup_center = spawn_pickup_center()
    collected = 0

    game_font = pygame.font.Font(None, 42)  # Fuente del _mod

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Input movimiento (lógica del original)
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = PLAYER_SPEED

        player_rect.x += dx
        player_rect.y += dy

        # Mantener dentro de la pantalla
        player_rect.clamp_ip(Rect(0, 0, WIDTH, HEIGHT))

        # Comprobar colisión: Rectángulo (Jugador) vs Círculo (Pickup)
        # Se usa una simplificación similar al original (distancia centro a centro)
        player_center = player_rect.center

        # Suma de la distancia necesaria para la colisión (radio del círculo + la mitad del lado más largo del rectángulo)
        # Esto no es una colisión perfecta Rect-Circle, pero es similar al original simple
        collision_distance = PICKUP_RADIUS + max(PLAYER_SIZE) // 2

        dist_sq = (player_center[0] - pickup_center[0]) ** 2 + \
            (player_center[1] - pickup_center[1]) ** 2

        if dist_sq <= collision_distance ** 2:
            collected += 1
            pickup_center = spawn_pickup_center()

        # Dibujado
        screen.fill(BACKGROUND_COLOR)

        # Dibujar pickup (Círculo)
        pygame.draw.circle(screen, PICKUP_COLOR, pickup_center, PICKUP_RADIUS)

        # Dibujar jugador (Rectángulo)
        pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

        # Texto contador
        score_text = game_font.render(f"Puntos: {collected}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
