import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Генерация точек (светлые цвета для лучшей видимости)
n_points = 10000
base_points = np.array([
    (np.random.uniform(0.001, 40), np.random.uniform(0, math.pi))
    for _ in range(n_points)
])

# Создание координат сетки
n_h_lines = 20  # Количество горизонтальных линий
n_v_lines = 100  # Количество вертикальных линий

# Координаты для линий сетки
horiz_y = np.linspace(0.01, math.pi - 0.1, n_h_lines)  # Y координаты горизонтальных линий
vert_x = np.linspace(0.01, 35, n_v_lines)                # X координаты вертикальных линий

# Точки для горизонтальных линий (каждая линия - 50 точек)
horiz_points_per_line = 50
horiz_x = np.linspace(0.01, 40, horiz_points_per_line)

# Точки для вертикальных линий (каждая линия - 50 точек)
vert_points_per_line = 50
vert_y = np.linspace(0.01, math.pi - 0.1, vert_points_per_line)

# Создаем массивы для исходных линий сетки
base_horiz_lines = []  # Исходные горизонтальные линии
base_vert_lines = []   # Исходные вертикальные линии

for y in horiz_y:
    line_points = np.array([(x, y) for x in horiz_x])
    base_horiz_lines.append(line_points)

for x in vert_x:
    line_points = np.array([(x, y) for y in vert_y])
    base_vert_lines.append(line_points)

# Преобразования точек
medium_points = np.array([(2 - 2*y/math.pi, 2*x/math.pi) for x, y in base_points])
final_points = np.array([(2*(1-x)/((1-x)**2 + y**2), 2*y/((1-x)**2 + y**2))
                         for x, y in medium_points])

# Преобразования горизонтальных линий сетки
medium_horiz_lines = []
final_horiz_lines = []

for line in base_horiz_lines:
    # Первое преобразование
    medium_line = np.array([(2 - 2*y/math.pi, 2*x/math.pi) for x, y in line])
    medium_horiz_lines.append(medium_line)

    # Второе преобразование
    final_line = np.array([(2*(1-x)/((1-x)**2 + y**2), 2*y/((1-x)**2 + y**2))
                           for x, y in medium_line])
    final_horiz_lines.append(final_line)

# Преобразования вертикальных линий сетки
medium_vert_lines = []
final_vert_lines = []

for line in base_vert_lines:
    # Первое преобразование
    medium_line = np.array([(2 - 2*y/math.pi, 2*x/math.pi) for x, y in line])
    medium_vert_lines.append(medium_line)

    # Второе преобразование
    final_line = np.array([(2*(1-x)/((1-x)**2 + y**2), 2*y/((1-x)**2 + y**2))
                           for x, y in medium_line])
    final_vert_lines.append(final_line)

# Создание графиков
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Настройка графиков
for ax, title, xlim, ylim in zip(axes,
                                 ['Исходные точки', 'После первого преобразования', 'После второго преобразования'],
                                 [(0, 8), (0, 4), (-4, 4)],
                                 [(0, 6), (0, 8), (0, 6)]):
    ax.set(xlabel='Re', ylabel='Im', title=title, aspect='equal', xlim=xlim, ylim=ylim)
    ax.grid(True, alpha=0.2, linestyle='--')  # Статичная фоновая сетка

# Точки (светлые пастельные цвета)
sc1 = axes[0].scatter([], [], s=2, color='#000000', alpha=0.5)
sc2 = axes[1].scatter([], [], s=2, color='#000000', alpha=0.5)
sc3 = axes[2].scatter([], [], s=2, color='#000000', alpha=0.5)

# Создание объектов для деформируемой сетки (горизонтальные и вертикальные линии)
horiz_lines_plots = []  # Горизонтальные линии для каждого графика
vert_lines_plots = []   # Вертикальные линии для каждого графика

grid_colors = ['#FF5555', '#5555FF', '#55CC55']  # Яркие цвета для сетки

for i, ax in enumerate(axes):
    # Создаем горизонтальные линии для этого графика
    h_lines = []
    for j in range(n_h_lines):
        line, = ax.plot([], [], color=grid_colors[i], linewidth=2.5,
                       alpha=0.9, zorder=5)
        h_lines.append(line)

    # Создаем вертикальные линии для этого графика
    v_lines = []
    for j in range(n_v_lines):
        line, = ax.plot([], [], color=grid_colors[i], linewidth=2.5,
                       alpha=0.9, zorder=5, linestyle='-')
        v_lines.append(line)

    horiz_lines_plots.append(h_lines)
    vert_lines_plots.append(v_lines)

# Функция анимации
def animate(frame):
    # Всегда показываем исходные точки
    sc1.set_offsets(base_points)

    if frame < 40:  # Первый этап - 40 кадров
        t = frame / 40

        # Точки - интерполяция между исходными и первым преобразованием
        interp_points = base_points * (1 - t) + medium_points * t
        sc2.set_offsets(interp_points)
        sc3.set_offsets(np.empty((0, 2)))  # Третий график пустой

        # Горизонтальные линии - интерполяция
        for j in range(n_h_lines):
            interp_line = base_horiz_lines[j] * (1 - t) + medium_horiz_lines[j] * t
            horiz_lines_plots[1][j].set_data(interp_line[:, 0], interp_line[:, 1])

        # Вертикальные линии - интерполяция
        for j in range(n_v_lines):
            interp_line = base_vert_lines[j] * (1 - t) + medium_vert_lines[j] * t
            vert_lines_plots[1][j].set_data(interp_line[:, 0], interp_line[:, 1])

        # Очищаем третий график
        for j in range(n_h_lines):
            horiz_lines_plots[2][j].set_data([], [])
        for j in range(n_v_lines):
            vert_lines_plots[2][j].set_data([], [])

    elif frame < 180:  # Второй этап - 50 кадров (дольше)
        t = (frame - 40) / 130

        # Точки
        sc2.set_offsets(medium_points)  # Второй график показывает полное первое преобразование
        interp_points = medium_points * (1 - t) + final_points * t
        sc3.set_offsets(interp_points)  # Третий график интерполирует

        # Второй график - полное первое преобразование сетки
        for j in range(n_h_lines):
            horiz_lines_plots[1][j].set_data(medium_horiz_lines[j][:, 0],
                                            medium_horiz_lines[j][:, 1])
        for j in range(n_v_lines):
            vert_lines_plots[1][j].set_data(medium_vert_lines[j][:, 0],
                                           medium_vert_lines[j][:, 1])

        # Третий график - интерполяция между первым и вторым преобразованием
        for j in range(n_h_lines):
            interp_line = medium_horiz_lines[j] * (1 - t) + final_horiz_lines[j] * t
            horiz_lines_plots[2][j].set_data(interp_line[:, 0], interp_line[:, 1])

        for j in range(n_v_lines):
            interp_line = medium_vert_lines[j] * (1 - t) + final_vert_lines[j] * t
            vert_lines_plots[2][j].set_data(interp_line[:, 0], interp_line[:, 1])

    else:  # Финальное состояние
        sc2.set_offsets(medium_points)
        sc3.set_offsets(final_points)

        # Второй график - полное первое преобразование
        for j in range(n_h_lines):
            horiz_lines_plots[1][j].set_data(medium_horiz_lines[j][:, 0],
                                            medium_horiz_lines[j][:, 1])
        for j in range(n_v_lines):
            vert_lines_plots[1][j].set_data(medium_vert_lines[j][:, 0],
                                           medium_vert_lines[j][:, 1])

        # Третий график - полное второе преобразование
        for j in range(n_h_lines):
            horiz_lines_plots[2][j].set_data(final_horiz_lines[j][:, 0],
                                            final_horiz_lines[j][:, 1])
        for j in range(n_v_lines):
            vert_lines_plots[2][j].set_data(final_vert_lines[j][:, 0],
                                           final_vert_lines[j][:, 1])

    # Собираем все объекты для обновления
    all_artists = [sc1, sc2, sc3]
    for lines in horiz_lines_plots:
        all_artists.extend(lines)
    for lines in vert_lines_plots:
        all_artists.extend(lines)

    return all_artists

# Инициализация
def init():
    sc1.set_offsets(np.empty((0, 2)))
    sc2.set_offsets(np.empty((0, 2)))
    sc3.set_offsets(np.empty((0, 2)))

    # Очищаем все линии сетки
    for i in range(3):
        for j in range(n_h_lines):
            horiz_lines_plots[i][j].set_data([], [])
        for j in range(n_v_lines):
            vert_lines_plots[i][j].set_data([], [])

    return []

# Запуск анимации
ani = FuncAnimation(fig, animate, init_func=init, frames=201, interval=50,
                   blit=True, repeat=True, cache_frame_data=False)
plt.tight_layout()
plt.show()