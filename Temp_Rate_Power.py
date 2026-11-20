import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Входные переменные
temperature = ctrl.Antecedent(np.arange(10, 36, 1), 'temperature')
rate = ctrl.Antecedent(np.arange(-2, 2.01, 0.1), 'rate')

# Выходная переменная
power = ctrl.Consequent(np.arange(-100, 101, 1), 'power')

# Функции принадлежности для temperature
temperature['cold'] = fuzz.trapmf(temperature.universe, [10, 10, 17, 20])
temperature['normal'] = fuzz.trimf(temperature.universe, [17, 22, 27])
temperature['hot'] = fuzz.trapmf(temperature.universe, [24, 28, 35, 35])

# Функции принадлежности для rate
rate['falling'] = fuzz.trimf(rate.universe, [-2, -2, 0])
rate['stable'] = fuzz.trimf(rate.universe, [-1, 0, 1])
rate['rising'] = fuzz.trimf(rate.universe, [0, 2, 2])

# Функции принадлежности для power
power['cool'] = fuzz.trapmf(power.universe, [-100, -100, -40, 0])
power['hold'] = fuzz.trimf(power.universe, [-30, 0, 30])
power['heat'] = fuzz.trapmf(power.universe, [0, 40, 100, 100])

# База правил
rule1 = ctrl.Rule(temperature['cold'] & rate['falling'], power['heat'])
rule2 = ctrl.Rule(temperature['cold'] & rate['stable'], power['heat'])
rule3 = ctrl.Rule(temperature['cold'] & rate['rising'], power['hold'])
rule4 = ctrl.Rule(temperature['normal'] & rate['falling'], power['heat'])
rule5 = ctrl.Rule(temperature['normal'] & rate['stable'], power['hold'])
rule6 = ctrl.Rule(temperature['normal'] & rate['rising'], power['cool'])
rule7 = ctrl.Rule(temperature['hot'] & rate['falling'], power['hold'])
rule8 = ctrl.Rule(temperature['hot'] & rate['stable'], power['cool'])
rule9 = ctrl.Rule(temperature['hot'] & rate['rising'], power['cool'])

power_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,
                                  rule5, rule6, rule7, rule8, rule9])
sim = ctrl.ControlSystemSimulation(power_ctrl)

# Прогон тестовых ситуаций
test_cases = [
    (12, -1.5, "Очень холодно, быстро падает"),
    (15, 0.0,  "Холодно, стабильно"),
    (19, 1.0,  "Прохладно, растёт"),
    (22, 0.0,  "Норма, стабильно"),
    (26, 0.5,  "Тепло, растёт"),
    (32, -0.5, "Жарко, падает"),
]

for t, r, desc in test_cases:
    sim.input['temperature'] = t
    sim.input['rate'] = r
    sim.compute()
    print(f"{desc:35s} | T={t:>2}, rate={r:>4} | power = {sim.output['power']:>7.2f}")
    

# # --- Анализ чувствительности по температуре (rate = 0) ---
# temps = np.arange(10, 36, 1)   # от 10 до 35 °C с шагом 1
# powers_temp = []

# for t in temps:
#     sim.input['temperature'] = t
#     sim.input['rate'] = 0.0    # фиксируем скорость изменения
#     sim.compute()
#     powers_temp.append(sim.output['power'])

# # Построение графика
# plt.figure(figsize=(8, 5))
# plt.plot(temps, powers_temp, marker='o', linestyle='-', color='b')
# plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # линия нуля
# plt.title('Зависимость выходной мощности от температуры (rate = 0)')
# plt.xlabel('Температура, °C')
# plt.ylabel('Мощность (power)')
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig('temp_sensitivity.png', dpi=200)
# plt.show()
# --- Анализ чувствительности по скорости (temperature = 22) ---
import matplotlib.pyplot as plt
import numpy as np

rates = np.linspace(-2.0, 2.0, 41)
powers_rate = []

for r in rates:
    sim.input['temperature'] = 22.0
    sim.input['rate'] = r
    try:
        sim.compute()
        p = sim.output['power']
        powers_rate.append(p)
        print(f"rate = {r:>5.1f} -> power = {p:>7.2f}") # Печатаем, чтобы видеть процесс
    except Exception as e:
        print(f"ОШИБКА при rate = {r:>5.1f}: {e}")
        powers_rate.append(0.0) # Если ошибка, записываем 0, чтобы график не ломался

# Теперь строим график
# plt.figure(figsize=(8, 5))
# plt.plot(rates, powers_rate, marker='o', markersize=3, linestyle='-', color='r')
# plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
# plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
# plt.title('Зависимость выходной мощности от скорости изменения (T = 22 °C)')
# plt.xlabel('Скорость изменения, °C/мин')
# plt.ylabel('Мощность (power)')
# plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()

def hard_threshold_controller(temp, rate):
    """Жёсткий пороговый регулятор для сравнения."""
    if temp < 20:
        return 100  # Включить нагрев на полную
    elif temp > 24:
        return -100 # Включить охлаждение на полную
    else:
        return 0    # Ничего не делать

print("\nСравнение нечёткой модели и жёсткого порога:")
print(f"{'Температура':>12} | {'Нечёткая':>10} | {'Жёсткая':>10}")
for t in [18, 19, 20, 21, 23, 24, 25]:
    sim.input['temperature'] = t
    sim.input['rate'] = 0.0
    sim.compute()
    fuzzy_val = sim.output['power']
    hard_val = hard_threshold_controller(t, 0.0)
    print(f"{t:>12} | {fuzzy_val:>10.2f} | {hard_val:>10}")