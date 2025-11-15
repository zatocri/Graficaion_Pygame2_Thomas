import pygame
import math

# Inicializar Pygame
pygame.init()
ventana = pygame.display.set_mode((800, 600))
# Nuevo color de fondo: Gris
gris_fondo = (50, 50, 50)
ROTATION_SPEED = 5  # grados por frame para suavizar el giro

# Cargar y redimensionar la imagen
# Asegúrate de tener la imagen "panda.jpg" en la misma carpeta
try:
    imagen_original = pygame.image.load("panda.jpg")
except pygame.error as e:
    print(f"Error al cargar imagen: {e}. Asegúrate de que 'panda.jpg' exista.")
    # Crea una superficie de reemplazo si falla la carga
    imagen_original = pygame.Surface((500, 500))
    imagen_original.fill((255, 150, 0))  # Fondo de color para verla

imagen = pygame.transform.scale(imagen_original, (500, 500))

# Posición central fija del objeto
center_x, center_y = 400, 300
current_angle = 0.0  # Ángulo actual del objeto


def normalize_angle_diff(current: float, target: float) -> float:
    """Normaliza la diferencia de ángulos a rango [-180, 180]."""
    diff = target - current
    while diff > 180:
        diff -= 360
    while diff < -180:
        diff += 360
    return diff


corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Obtener posición del ratón y calcular ángulo objetivo
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # math.atan2 da el ángulo en radianes desde el eje X (derecha)
    target_angle_rad = math.atan2(mouse_y - center_y, mouse_x - center_x)
    # Convertir a grados y ajustar para que 0 grados apunte hacia arriba (-90)
    target_angle_deg = math.degrees(target_angle_rad) + 90

    # Suavizar la rotación hacia el objetivo
    angle_diff = normalize_angle_diff(current_angle, target_angle_deg)

    if abs(angle_diff) < ROTATION_SPEED:
        current_angle = target_angle_deg
    else:
        current_angle += ROTATION_SPEED if angle_diff > 0 else -ROTATION_SPEED

    # Rotar la imagen redimensionada
    imagen_rotada = pygame.transform.rotate(imagen, -current_angle)

    # Dibujar
    ventana.fill(gris_fondo)
    ventana.blit(imagen_rotada, (center_x - imagen_rotada.get_width() //
                 2, center_y - imagen_rotada.get_height() // 2))
    pygame.display.flip()

    keys = pygame.key.get_pressed()

    # *** CAMBIOS AQUÍ para usar + y - ***
    if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
        imagen = pygame.transform.scale(
            imagen, (imagen.get_width() + 5, imagen.get_height() + 5))
    if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
        imagen = pygame.transform.scale(
            imagen, (imagen.get_width() - 5, imagen.get_height() - 5))

    # Limitar tamaño mínimo
    if imagen.get_width() < 100 or imagen.get_height() < 100:
        imagen = pygame.transform.scale(imagen, (100, 100))
    # Tecla Esc para salir
    if keys[pygame.K_ESCAPE]:
        corriendo = False
pygame.quit()
