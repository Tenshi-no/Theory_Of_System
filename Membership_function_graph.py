import numpy as np
import matplotlib.pyplot as plt

def trimf(x, a, b, c):
    """Треугольная функция принадлежности."""
    y = np.zeros_like(x)
    left = (x >= a) & (x <= b)
    right = (x > b) & (x <= c)
    y[left] = (x[left] - a) / (b - a)
    y[right] = (c - x[right]) / (c - b)
    return y

def trapmf(x, a, b, c, d):
    """Трапециевидная функция принадлежности."""
    y = np.zeros_like(x)
    y[(x >= a) & (x <= b)] = (x[(x >= a) & (x <= b)] - a) / (b - a) if b != a else 1
    y[(x >= b) & (x <= c)] = 1
    y[(x >= c) & (x <= d)] = (d - x[(x >= c) & (x <= d)]) / (d - c) if d != c else 1
    return y

# --- Температура ---
x_temp = np.linspace(10, 35, 500)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x_temp, trapmf(x_temp, 10, 10, 17, 20), label='холодно')
ax.plot(x_temp, trimf(x_temp, 17, 22, 27), label='нормально')
ax.plot(x_temp, trapmf(x_temp, 24, 28, 35, 35), label='жарко')
ax.set_xlabel('Температура, °C'); ax.set_ylabel('Степень принадлежности')
ax.set_title('Функции принадлежности переменной temperature')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig('temp_mf.png', dpi=200); plt.show()

# --- Скорость изменения ---
x_rate = np.linspace(-2, 2, 500)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x_rate, trimf(x_rate, -2, -2, 0), label='падает')
ax.plot(x_rate, trimf(x_rate, -1, 0, 1), label='стабильно')
ax.plot(x_rate, trimf(x_rate, 0, 2, 2), label='растёт')
ax.set_xlabel('Скорость изменения, °C/мин'); ax.set_ylabel('Степень принадлежности')
ax.set_title('Функции принадлежности переменной rate')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig('rate_mf.png', dpi=200); plt.show()

# --- Мощность ---
x_power = np.linspace(-100, 100, 500)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x_power, trapmf(x_power, -100, -100, -40, 0), label='охлаждать')
ax.plot(x_power, trimf(x_power, -30, 0, 30), label='поддерживать')
ax.plot(x_power, trapmf(x_power, 0, 40, 100, 100), label='нагревать')
ax.set_xlabel('Мощность'); ax.set_ylabel('Степень принадлежности')
ax.set_title('Функции принадлежности переменной power')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig('power_mf.png', dpi=200); plt.show()