import pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
blanco = (255, 255, 255)
# Nuevo color: Magenta
magenta = (255, 0, 255)
x, y = 400, 300
reloj = pygame.time.Clock()
corriendo = True

# Parámetros para la pulsación modificados
radio = 25      # radio inicial
dr = 2          # cambio de radio por frame (más rápido)
RADIO_MIN = 20  # Límite inferior modificado
RADIO_MAX = 50  # Límite superior modificado

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Actualizar radio: crecer o encoger
    radio += dr
    # Cambiar dirección si alcanzamos los límites
    if radio >= RADIO_MAX:
        radio = RADIO_MAX
        dr = -abs(dr)
    elif radio <= RADIO_MIN:
        radio = RADIO_MIN
        dr = abs(dr)

    ventana.fill(blanco)
    pygame.draw.circle(ventana, magenta, (x, y), int(radio)
                       )  # Dibujamos el círculo magenta
    pygame.display.flip()

    reloj.tick(60)  # 60 FPS
pygame.quit()
