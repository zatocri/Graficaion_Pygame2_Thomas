import pygame
import random

pygame.init()
ventana = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Mi primera ventana")

corriendo = True

# Color inicial
color_fondo = (135, 206, 250)

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Detectar cuando presionas una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_c:  # Si la tecla es C...
                # Generar un nuevo color aleatorio
                color_fondo = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                print("Nuevo color:", color_fondo)

    ventana.fill(color_fondo)

    pygame.display.update()

pygame.quit()
