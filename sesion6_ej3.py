"""
Juego de evasión: mueve un rectángulo para evitar círculos móviles. (FINAL)

El jugador (RECTÁNGULO) debe evitar los círculos enemigos móviles.
Si colisiona, el juego termina y puede ser reiniciado con la tecla R.
"""

import sys
import random
import pygame

# Configuración
WIDTH, HEIGHT = 900, 700
FPS = 50

# Jugador (RECTÁNGULO - Requerimiento cumplido)
PLAYER_W, PLAYER_H = 50, 50  # Tamaño del rectángulo
PLAYER_SPEED = 6
PLAYER_COLOR = (255, 200, 0)  # Jugador amarillo

# Círculos enemigos
ENEMY_RADIUS = 30
ENEMY_SPEED = 4
ENEMY_COLOR = (0, 150, 255)  # Enemigos azules
INITIAL_ENEMIES = 4

BACKGROUND_COLOR = (30, 50, 50)

pygame.init()


def create_enemy_data(existing_enemies: list) -> dict:
    """Genera un nuevo círculo en posición aleatoria, evitando superposición."""
    while True:
        x = random.randint(ENEMY_RADIUS, WIDTH - ENEMY_RADIUS)
        y = random.randint(ENEMY_RADIUS, HEIGHT // 3)

        # Verificar que no solape con otros enemigos
        valid = True
        for enemy in existing_enemies:
            dist = ((x - enemy['x']) ** 2 + (y - enemy['y']) ** 2) ** 0.5
            if dist < ENEMY_RADIUS * 3.5:
                valid = False
                break

        if valid:
            break

    direction = random.choice([-1, 1])
    return {
        'x': float(x),
        'y': float(y),
        'vx': ENEMY_SPEED * direction,
        'vy': random.uniform(-1, 1) * 2.0,
    }


def check_collision(player_rect: pygame.Rect, enemies: list) -> bool:
    """Verifica si el jugador (RECTÁNGULO) colisiona con algún círculo (CÍRCULO)."""
    for enemy in enemies:
        # Centro del círculo
        circle_center = (enemy['x'], enemy['y'])

        # Punto más cercano del rectángulo al círculo (lógica de colisión Rect-Circle)
        closest_x = max(player_rect.left, min(
            circle_center[0], player_rect.right))
        closest_y = max(player_rect.top, min(
            circle_center[1], player_rect.bottom))

        # Distancia
        dx = circle_center[0] - closest_x
        dy = circle_center[1] - closest_y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < ENEMY_RADIUS:
            return True

    return False


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evasión (Jugador Rectángulo)")
    clock = pygame.time.Clock()

    game_over = False
    score_frames = 0

    # Jugador (RECTÁNGULO)
    player_x = WIDTH // 2 - PLAYER_W // 2
    player_y = HEIGHT - 50 - PLAYER_H // 2

    # Enemigos
    enemies = [create_enemy_data([]) for _ in range(INITIAL_ENEMIES)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            # Input del jugador
            keys = pygame.key.get_pressed()
            move_speed = PLAYER_SPEED

            # Aceleración con Shift
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                move_speed *= 2

            # Movimiento del rectángulo
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x -= move_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x += move_speed
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_y -= move_speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_y += move_speed

            # Limitar jugador en pantalla
            player_x = max(0, min(player_x, WIDTH - PLAYER_W))
            player_y = max(0, min(player_y, HEIGHT - PLAYER_H))

            # Actualizar enemigos (lógica sin cambios)
            for enemy in enemies:
                enemy['x'] += enemy['vx']
                enemy['y'] += enemy['vy']

                if enemy['x'] - ENEMY_RADIUS < 0 or enemy['x'] + ENEMY_RADIUS > WIDTH:
                    enemy['vx'] *= -1
                if enemy['y'] - ENEMY_RADIUS < 0 or enemy['y'] + ENEMY_RADIUS > HEIGHT:
                    enemy['vy'] *= -1

                enemy['x'] = max(ENEMY_RADIUS, min(
                    enemy['x'], WIDTH - ENEMY_RADIUS))
                enemy['y'] = max(ENEMY_RADIUS, min(
                    enemy['y'], HEIGHT - ENEMY_RADIUS))

            # Verificar colisión
            player_rect = pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H)
            if check_collision(player_rect, enemies):
                game_over = True
                print(
                    f"¡Colisión! Score final: {score_frames // FPS} segundos")

        # Dibujado
        screen.fill(BACKGROUND_COLOR)

        if not game_over:
            # Dibujar jugador (RECTÁNGULO)
            player_rect = pygame.Rect(player_x, player_y, PLAYER_W, PLAYER_H)
            pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
            pygame.draw.rect(screen, (200, 150, 0), player_rect, 2)

            # Dibujar enemigos (Círculos)
            for enemy in enemies:
                pygame.draw.circle(screen, ENEMY_COLOR, (int(
                    enemy['x']), int(enemy['y'])), ENEMY_RADIUS)
                pygame.draw.circle(screen, (50, 100, 200), (int(
                    enemy['x']), int(enemy['y'])), ENEMY_RADIUS, 2)

            score_frames += 1
        else:
            # Pantalla de game over
            font_large = pygame.font.Font(None, 60)
            font_small = pygame.font.Font(None, 36)

            text_gameover = font_large.render(
                "FIN DEL JUEGO", True, (255, 100, 100))
            text_score = font_small.render(
                f"Tiempo Sobrevivido: {score_frames // FPS}s", True, (255, 255, 255))
            text_restart = font_small.render(
                "Presiona R para reiniciar", True, (150, 150, 150))

            screen.blit(text_gameover, (WIDTH // 2 -
                        text_gameover.get_width() // 2, 150))
            screen.blit(text_score, (WIDTH // 2 -
                        text_score.get_width() // 2, 250))
            screen.blit(text_restart, (WIDTH // 2 -
                        text_restart.get_width() // 2, 350))

            keys = pygame.key.get_pressed()
            # Reiniciar con R
            if keys[pygame.K_r]:
                game_over = False
                score_frames = 0
                player_x = WIDTH // 2 - PLAYER_W // 2
                player_y = HEIGHT - 50 - PLAYER_H // 2
                enemies = [create_enemy_data([])
                           for _ in range(INITIAL_ENEMIES)]

        # Mostrar score/tiempo en pantalla
        if not game_over:
            font = pygame.font.Font(None, 28)
            time_text = font.render(
                f"Tiempo: {score_frames // FPS}s", True, (255, 255, 255))
            screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
