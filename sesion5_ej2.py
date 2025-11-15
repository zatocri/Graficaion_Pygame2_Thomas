import sys
from pathlib import Path
import pygame

# --- Configuración MODIFICADA ---
SPRITESHEET_NAME = "spritesheet.png"
FRAME_W = 128  # Ancho de cada frame (128 píxeles, ya que hay 2 por fila)
FRAME_H = 128  # Alto de cada frame (128 píxeles, ya que hay 2 por columna)
# 100 ms por frame (puedes ajustar si la animación es muy lenta o rápida)
FRAME_DURATION_MS = 100

WIDTH, HEIGHT = 800, 600  # Mantener un tamaño de ventana decente
FPS = 60
# --- Función de Carga (sin cambios) ---


def load_frames_from_sheet(sheet: pygame.Surface, w: int, h: int):
    frames = []
    sheet_w, sheet_h = sheet.get_size()
    cols = sheet_w // w
    rows = sheet_h // h
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * w, row * h, w, h)
            frame = sheet.subsurface(rect).copy()
            frames.append(frame)
    return frames


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    script_dir = Path(__file__).resolve().parent
    sheet_path = script_dir / SPRITESHEET_NAME
    if not sheet_path.exists():
        print(f"Error: sprite sheet no encontrada: {sheet_path}")
        print("Asegúrate de que el archivo esté en la misma carpeta que el script.")
        pygame.quit()
        return

    sheet = pygame.image.load(str(sheet_path)).convert_alpha()
    frames = load_frames_from_sheet(sheet, FRAME_W, FRAME_H)
    if not frames:
        print("No se extrajeron frames. Revisa FRAME_W / FRAME_H.")
        pygame.quit()
        return

    current_frame = 0
    last_update = pygame.time.get_ticks()

    x = WIDTH // 2
    y = HEIGHT // 2

    SCALE_FACTOR = 2  # Nuevo: Escalar la animación al doble

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Actualizar frame (lógica sin cambios)
        now = pygame.time.get_ticks()
        if now - last_update >= FRAME_DURATION_MS:
            current_frame = (current_frame + 1) % len(frames)
            last_update = now

        # Dibujar
        screen.fill((20, 20, 20))  # Fondo más oscuro
        frame_surf = frames[current_frame]

        # Escalar el frame antes de dibujarlo
        frame_surf = pygame.transform.scale(
            frame_surf, (FRAME_W * SCALE_FACTOR, FRAME_H * SCALE_FACTOR))

        rect = frame_surf.get_rect(center=(x, y))
        screen.blit(frame_surf, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
