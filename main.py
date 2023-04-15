import sys
import pygame as pg
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from simulation import Simulation

pg.init()

# Colores
BLACK = (0, 0, 0)
GRAY = (65, 65, 65)
WHITE = (255, 255, 255)
PINK = (255, 207, 224)
LBLUE = (135, 206, 235)

# Inicialización de la ventana
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('')

# Variables
clock = pg.time.Clock()
run = False

simulation = Simulation(screen)

# Bucle principal
while not run:
    # Manejo de eventos del juego
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = True

    screen.fill(GRAY)
    # Code
    simulation.update()

    pg.display.flip()
    clock.tick(FPS)

# Cierre del bucle
pg.quit()
sys.exit()
