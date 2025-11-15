import sys
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.7  # aceleración por frame incrementada (cae más rápido)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    x = WIDTH // 2
    y = 50.0
    radius = 40  # Radio ligeramente mayor
    vy = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Física: gravedad
        vy += GRAVITY
        y += vy

        # Rebote en el suelo con pérdida de velocidad reducida (rebota más alto)
        ground = HEIGHT
        if y + radius >= ground:
            y = ground - radius
            vy = -vy * 0.9  # Rebote con solo 10% de pérdida (antes era 20%)
            if abs(vy) < 0.1:
                vy = 0.0

        # Dibujado
        screen.fill((200, 200, 200))  # Fondo gris claro
        # Línea del suelo de diferente color
        pygame.draw.line(screen, (50, 50, 50),
                         (0, HEIGHT - 1), (WIDTH, HEIGHT - 1), 3)
        # Círculo verde
        pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), radius)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
