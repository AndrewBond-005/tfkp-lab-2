import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

n_points = 20000
base = np.array([(np.random.uniform(0.001, 40), np.random.uniform(0, math.pi)) for _ in range(n_points)])

def f_direct(x, y):
    """Прямое преобразование f: Ω → G"""
    z = x + 1j * y
    w = -2 / (1 + (2j / np.pi) * z)
    return w.real, w.imag


def g_inverse(u, v):
    """Обратное преобразование g: G → Ω"""
    w = u + 1j * v
    z = -(np.pi / (2j)) * (1 + 2 / w)
    return z.real, z.imag


final_x, final_y = f_direct(base[:, 0], base[:, 1])
final = np.column_stack([final_x, final_y])
base2_x, base2_y = g_inverse(final[:, 0], final[:, 1])
base2 = np.column_stack([base2_x, base2_y])
fig, ax = plt.subplots(figsize=(8, 6))
ax.set(xlabel='Re', ylabel='Im', title='Конформное отображение $f(z) = -\\dfrac{2}{1 + \\frac{2i}{\pi}z}$',
       aspect='equal', xlim=(-4, 8), ylim=(-1, 7))
ax.grid(True, alpha=0.3)
sc = ax.scatter(base[:, 0], base[:, 1], s=2, color='blue', alpha=0.7)
theta = np.linspace(0, np.pi, 100)
ax.plot(1 + np.cos(theta), np.sin(theta), 'k--', alpha=0.7, linewidth=1)
ax.plot(-1 + np.cos(theta), np.sin(theta), 'k--', alpha=0.7, linewidth=1)


def animate(frame):
    if frame < 40:
        t = frame / 40
        points = base * (1 - t) + final * t
        title_text = f'Прямое преобразование: Ω → G ({t * 100:.0f}%)'

    elif frame < 60:
        points = final
        t_pause = (frame - 40) / 20
        alpha_pulse = 0.7 + 0.3 * np.sin(t_pause * np.pi * 2)
        sc.set_alpha(alpha_pulse)
        title_text = 'Область G (пауза)'

    elif frame < 100:
        t = (frame - 60) / 40
        points = final * (1 - t) + base2 * t
        sc.set_alpha(0.7)
        title_text = f'Обратное преобразование: G → Ω ({t * 100:.0f}%)'

    else:
        points = base2
        t_pause = (frame - 100) / 20
        alpha_pulse = 0.7 + 0.3 * np.sin(t_pause * np.pi * 2)
        sc.set_alpha(alpha_pulse)
        title_text = 'Область Ω (возврат)'

    sc.set_offsets(points)
    ax.set_title(title_text)
    return [sc]



ani = FuncAnimation(fig, animate, frames=120, interval=50, blit=True, repeat=True)

plt.tight_layout()
plt.show()
