import pygame
pygame.init()

# Configuración y colores
SCREEN_W, SCREEN_H = 800, 600
ventana = pygame.display.set_mode((SCREEN_W, SCREEN_H))
WHITE = (255, 255, 255)
PURPLE = (150, 50, 200)  # Nuevo color para el jugador
ORANGE = (255, 150, 0)  # Nuevo color para el objetivo
GREEN_HIT = (0, 200, 50)
FONT_COLOR = (30, 30, 30)

# Fuente para mostrar texto en pantalla
font = pygame.font.Font(None, 40)  # Tamaño de fuente ligeramente mayor

# Jugador
player_rect = pygame.Rect(400, 300, 60, 60)  # Jugador más grande
# Posición y tamaño diferentes para el objetivo
target_rect = pygame.Rect(100, 100, 40, 40)

# Velocidad en píxeles por frame
MOVEMENT_SPEED = 8  # Velocidad ajustada para movimiento basado en FPS
FPS = 60
clock = pygame.time.Clock()

# Posición en float para movimiento suave independiente de FPS
player_x = float(player_rect.x)
player_y = float(player_rect.y)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Movimiento basado en FPS (más simple que dt)
    if keys[pygame.K_LEFT]:
        player_x -= MOVEMENT_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += MOVEMENT_SPEED
    if keys[pygame.K_UP]:
        player_y -= MOVEMENT_SPEED
    if keys[pygame.K_DOWN]:
        player_y += MOVEMENT_SPEED

    # Limitar jugador dentro de los bordes de la ventana
    player_x = max(0, min(player_x, SCREEN_W - player_rect.width))
    player_y = max(0, min(player_y, SCREEN_H - player_rect.height))

    # Sincronizar rect con la posición
    player_rect.x = int(player_x)
    player_rect.y = int(player_y)

    # Dibujado
    ventana.fill(WHITE)
    pygame.draw.rect(ventana, ORANGE, target_rect)  # Dibujar objetivo

    current_player_color = PURPLE
    if player_rect.colliderect(target_rect):
        # Cambiar color del jugador y mostrar mensaje de colisión
        current_player_color = GREEN_HIT
        text_surface = font.render("¡OBJETIVO ALCANZADO!", True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_W // 2, 50))
        ventana.blit(text_surface, text_rect)

    pygame.draw.rect(ventana, current_player_color, player_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
