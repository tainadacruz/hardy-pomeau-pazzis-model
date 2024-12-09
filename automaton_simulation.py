import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros
GRID_SIZE = 20
STEPS = 50
INTERVAL = 500

# Direções
UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

# Inicialização
grid = np.zeros((GRID_SIZE, GRID_SIZE, 8), dtype=int)

center = GRID_SIZE // 2
radius = GRID_SIZE // 4

for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if (x - center)**2 + (y - center)**2 < radius**2:  # Checa se está dentro do raio
            # Cada direção terá 50% de chance de ser ocupada
            if np.random.rand() < 0.5:
                grid[x, y, UP] = 1
            if np.random.rand() < 0.5:
                grid[x, y, DOWN] = 1
            if np.random.rand() < 0.5:
                grid[x, y, LEFT] = 1
            if np.random.rand() < 0.5:
                grid[x, y, RIGHT] = 1
            if np.random.rand() < 0.5:
                grid[x, y, UP_RIGHT] = 1
            if np.random.rand() < 0.5:
                grid[x, y, DOWN_RIGHT] = 1
            if np.random.rand() < 0.5:
                grid[x, y, DOWN_LEFT] = 1
            if np.random.rand() < 0.5:
                grid[x, y, UP_LEFT] = 1


def count_particles(g):
    """Conta o número total de partículas na grade."""
    return np.sum(g)

def stream(g):
    """Etapa de movimentação: partículas se movem na direção em que estão viajando."""

    new_grid = np.zeros_like(g)
    
    # UP
    new_grid[:-1, :, UP] = g[1:, :, UP]
    new_grid[-1, :, UP] = g[0, :, UP]
    
    # DOWN
    new_grid[1:, :, DOWN] = g[:-1, :, DOWN]
    new_grid[0, :, DOWN] = g[-1, :, DOWN]
    
    # LEFT
    new_grid[:, :-1, LEFT] = g[:, 1:, LEFT]
    new_grid[:, -1, LEFT] = g[:, 0, LEFT]
    
    # RIGHT
    new_grid[:, 1:, RIGHT] = g[:, :-1, RIGHT]
    new_grid[:, 0, RIGHT] = g[:, -1, RIGHT]
    
    # UP_RIGHT
    new_grid[:-1, 1:, UP_RIGHT] = g[1:, :-1, UP_RIGHT]
    new_grid[-1, 1:, UP_RIGHT] = g[0, :-1, UP_RIGHT]
    new_grid[:-1, 0, UP_RIGHT] = g[1:, -1, UP_RIGHT]
    new_grid[-1, 0, UP_RIGHT] = g[0, -1, UP_RIGHT]
    
    # DOWN_RIGHT
    new_grid[1:, 1:, DOWN_RIGHT] = g[:-1, :-1, DOWN_RIGHT]
    new_grid[0, 1:, DOWN_RIGHT] = g[-1, :-1, DOWN_RIGHT]
    new_grid[1:, 0, DOWN_RIGHT] = g[:-1, -1, DOWN_RIGHT]
    new_grid[0, 0, DOWN_RIGHT] = g[-1, -1, DOWN_RIGHT]
    
    # DOWN_LEFT
    new_grid[1:, :-1, DOWN_LEFT] = g[:-1, 1:, DOWN_LEFT]
    new_grid[0, :-1, DOWN_LEFT] = g[-1, 1:, DOWN_LEFT]
    new_grid[1:, -1, DOWN_LEFT] = g[:-1, 0, DOWN_LEFT]
    new_grid[0, -1, DOWN_LEFT] = g[-1, 0, DOWN_LEFT]
    
    # UP_LEFT
    new_grid[:-1, :-1, UP_LEFT] = g[1:, 1:, UP_LEFT]
    new_grid[-1, :-1, UP_LEFT] = g[0, 1:, UP_LEFT]
    new_grid[:-1, -1, UP_LEFT] = g[1:, 0, UP_LEFT]
    new_grid[-1, -1, UP_LEFT] = g[0, 0, UP_LEFT]

    return new_grid

def collide(g):
    """ 
    Resolve colisões considerando 8 direções.
    - Caso haja pares opostos, transformam-se em pares perpendiculares.
    - Caso haja 4 partículas formando um cruzamento, faz rotação.
    - Para diagonais, segue a mesma lógica.
    - Em casos mais complexos, tenta manter o número de partículas e distribuir de forma coerente.
    """
    new_grid = np.zeros_like(g)
    count = np.sum(g, axis=2)

    # Máscaras de presença
    up = g[:, :, UP] == 1
    down = g[:, :, DOWN] == 1
    left = g[:, :, LEFT] == 1
    right = g[:, :, RIGHT] == 1
    ur = g[:, :, UP_RIGHT] == 1
    dr = g[:, :, DOWN_RIGHT] == 1
    dl = g[:, :, DOWN_LEFT] == 1
    ul = g[:, :, UP_LEFT] == 1

    # Define pares opostos:
    #  Oposto de UP é DOWN
    #  Oposto de RIGHT é LEFT
    #  Oposto de UP_RIGHT é DOWN_LEFT
    #  Oposto de DOWN_RIGHT é UP_LEFT
    vertical_pair = (count == 2) & up & down
    horizontal_pair = (count == 2) & left & right
    diag_pair_ur_dl = (count == 2) & ur & dl
    diag_pair_dr_ul = (count == 2) & dr & ul

    # UP/DOWN -> LEFT/RIGHT
    new_grid[vertical_pair, LEFT] = 1
    new_grid[vertical_pair, RIGHT] = 1

    # LEFT/RIGHT -> UP/DOWN
    new_grid[horizontal_pair, UP] = 1
    new_grid[horizontal_pair, DOWN] = 1

    # UP_RIGHT/DOWN_LEFT -> DOWN_RIGHT/UP_LEFT (rotação 90 graus)
    new_grid[diag_pair_ur_dl, DOWN_RIGHT] = 1
    new_grid[diag_pair_ur_dl, UP_LEFT] = 1

    # DOWN_RIGHT/UP_LEFT -> UP_RIGHT/DOWN_LEFT
    new_grid[diag_pair_dr_ul, UP_RIGHT] = 1
    new_grid[diag_pair_dr_ul, DOWN_LEFT] = 1

    # 4 partículas formando cruz + diagonais:
    # Considera o caso de 4 partículas simples (UP, DOWN, LEFT, RIGHT):
    four_basic = (count == 4) & up & down & left & right
    # Rotaciona: UP->LEFT, RIGHT->UP, DOWN->RIGHT, LEFT->DOWN
    new_grid[four_basic, LEFT] = up[four_basic]
    new_grid[four_basic, UP] = right[four_basic]
    new_grid[four_basic, RIGHT] = down[four_basic]
    new_grid[four_basic, DOWN] = left[four_basic]

    # 4 diagonais: UR, DR, DL, UL
    four_diag = (count == 4) & ur & dr & dl & ul
    # Rotaciona: UR->DR, DR->DL, DL->UL, UL->UR
    new_grid[four_diag, DOWN_RIGHT] = ur[four_diag]
    new_grid[four_diag, DOWN_LEFT] = dr[four_diag]
    new_grid[four_diag, UP_LEFT] = dl[four_diag]
    new_grid[four_diag, UP_RIGHT] = ul[four_diag]

    # 1,3,5,6,7,8 partículas ou combinações não tratadas acima:
    # Conserva as partículas originais (sem colisão definida)
    no_collision = ~ (vertical_pair | horizontal_pair | diag_pair_ur_dl | diag_pair_dr_ul | four_basic | four_diag)
    
    # Células sem colisão: conserva o estado original
    new_grid[no_collision] = g[no_collision]

    return new_grid

# Configura o gráfico
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(np.sum(grid, axis=2), cmap="Blues", origin="upper")
particles = count_particles(grid)
ax.set_title(f"Simulação HPP | Passo 0 | Partículas = {particles}")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.colorbar(im, ax=ax, label="Densidade de Partículas")


def update(frame):
    """Atualiza o gráfico a cada passo."""
    global grid
    grid = stream(grid)
    grid = collide(grid)
    
    particles = count_particles(grid)
    
    im.set_array(np.sum(grid, axis=2))
    ax.set_title(f"Simulação HPP | Passo {frame} | Partículas = {particles}")
    return [im]


ani = FuncAnimation(fig, update, frames=STEPS, interval=INTERVAL, blit=False)
plt.show()
