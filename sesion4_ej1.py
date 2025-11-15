import pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
# Nuevo color: Azul
azul = (0, 0, 255)
blanco = (255, 255, 255)
x, y = 400, 300
velocidad_x = 7  # Velocidad inicial un poco mayor
reloj = pygame.time.Clock()
corriendo = True
radio_circulo = 50  # Nuevo radio
BORDE_IZQUIERDO = radio_circulo
BORDE_DERECHO = 800 - radio_circulo

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    x += velocidad_x

    # Rebote en los límites con radio_circulo
    if x >= BORDE_DERECHO or x <= BORDE_IZQUIERDO:
        velocidad_x = -velocidad_x  # Invierte la dirección

        # Aumenta la velocidad en un factor constante de 1.1 en cada rebote
        # Usamos abs() para asegurar que el incremento se aplique a la magnitud
        if velocidad_x > 0:
            velocidad_x = abs(velocidad_x) * 1.05
        else:
            velocidad_x = -abs(velocidad_x) * 1.05

    ventana.fill(blanco)
    # Dibujamos el círculo azul
    pygame.draw.circle(ventana, azul, (x, y), radio_circulo)
    pygame.display.flip()
    reloj.tick(60)  # 60 FPS
pygame.quit()
