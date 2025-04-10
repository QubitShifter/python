import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


params = {
    'solar_luminosity_min': 0.3,
    'solar_luminosity_max': 1.5,
    'solar_luminosity_step': 0.02,
    'temp_optimal': 22.5,
    'temp_white': 15.0,
    'temp_black': 40.0,
    'albedo_white': 0.25,
    'albedo_black': 0.75,
    'albedo_barren': 0.5,
    'growth_rate_max': 1.0,
    'mortality_rate': 0.01,
}

# категории за отделните темпшератури
def classify_temperature_grid(grid, T_barren, T_white, T_black):
    classified_grid = np.zeros_like(grid, dtype=int)
    for i in range(grid.shape[0]): #итерации по ред
        for j in range(grid.shape[1]):  #итерации по колони
            temp = grid[i, j]
            if np.isclose(temp, T_barren, atol=0.1):
                classified_grid[i, j] = 0  # Barren land
            elif np.isclose(temp, T_white, atol=0.1):
                classified_grid[i, j] = 1  # White daisies
            elif np.isclose(temp, T_black, atol=0.1):
                classified_grid[i, j] = 2  # Black daisies
    return classified_grid

# Growth rate
def growth_rate(temperature, temp_optimal):
    return max(0.0, 1 - 0.003265 * (temp_optimal - temperature) ** 2)

# Слънчева светимост
solar_luminosities = np.arange(params['solar_luminosity_min'],
                               params['solar_luminosity_max'] + params['solar_luminosity_step'],
                               params['solar_luminosity_step'])

area_white = []
area_black = []
area_barren = []
temp_with_daisies = []
temp_barren = []
temperature_grids = []

# ОДУ
def daisy_system(t, y, S):
    A_w, A_b = y
    A_barren = max(0.0, 1.0 - A_w - A_b)

    T_white = 30 * S * (1 - params['albedo_white']) ** 0.25
    T_black = 30 * S * (1 - params['albedo_black']) ** 0.25

    growth_white = growth_rate(T_white, params['temp_optimal'])
    growth_black = growth_rate(T_black, params['temp_optimal'])

    dA_w_dt = A_w * (growth_white * A_barren) - params['mortality_rate'] * A_w
    dA_b_dt = A_b * (growth_black * A_barren) - params['mortality_rate'] * A_b

    return [dA_w_dt, dA_b_dt]

# Simulation loop
for S in solar_luminosities:
    # Solve the differential equations
    sol = solve_ivp(
        daisy_system,
        [0, 100],  # Simulate over time from 0 to 100
        [0.2, 0.2],  # Initial areas of white and black daisies
        args=(S,),
        t_eval=np.linspace(0, 100, 500)
    )

    # Final areas (steady state)
    A_w_final, A_b_final = sol.y[0, -1], sol.y[1, -1]

    # Ensure areas are non-negative
    A_w_final = max(0.0, A_w_final)
    A_b_final = max(0.0, A_b_final)
    A_barren_final = max(0.0, 1.0 - A_w_final - A_b_final)

    # Нормализиране
    total_area = A_w_final + A_b_final + A_barren_final
    if total_area > 0:
        A_w_final /= total_area
        A_b_final /= total_area
        A_barren_final /= total_area
    else:
        A_w_final = A_b_final = A_barren_final = 0.0

    # Температура
    planetary_albedo = (A_w_final * params['albedo_white'] +
                        A_b_final * params['albedo_black'] +
                        A_barren_final * params['albedo_barren'])

    if planetary_albedo < 0 or planetary_albedo > 1:
        planetary_albedo = params['albedo_barren']  # Fallback in case of invalid value

    T_planetary = 30 * S * (1 - planetary_albedo) ** 0.25

    # Температура е завизимост от заселеността
    T_barren = 30 * S * (1 - params['albedo_barren']) ** 0.25
    T_white = 30 * S * (1 - params['albedo_white']) ** 0.25
    T_black = 30 * S * (1 - params['albedo_black']) ** 0.25

    # Разпределение по температура
    temperature_grid = np.random.choice(
        [T_barren, T_white, T_black],
        size=(50, 50),
        p=[A_barren_final, A_w_final, A_b_final]
    )

    # запазване на резултатите
    area_white.append(A_w_final)
    area_black.append(A_b_final)
    area_barren.append(A_barren_final)
    temp_with_daisies.append(T_planetary)
    temp_barren.append(T_barren)
    temperature_grids.append(temperature_grid)

#
area_white = np.array(area_white)
area_black = np.array(area_black)
area_barren = np.array(area_barren)
temp_with_daisies = np.array(temp_with_daisies)
temp_barren = np.array(temp_barren)

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# % Площ спрямо слънчева светимост
axes[0, 0].plot(solar_luminosities, area_white, label='White Daisies', color='green')
axes[0, 0].plot(solar_luminosities, area_black, label='Black Daisies', color='black')
axes[0, 0].plot(solar_luminosities, area_barren, label='Barren Land', color='brown')
axes[0, 0].set_title('Площ спрямо слънчева светимост [%]', fontsize=12)
axes[0, 0].set_xlabel('слънчева светимост', fontsize=10)
axes[0, 0].set_ylabel('Площ [%]', fontsize=10)
axes[0, 0].legend()
axes[0, 0].grid(True)

# Популация на маргаритките
color_map = {
    0: [139 / 255, 69 / 255, 19 / 255],  # Barren land
    1: [1, 1, 1],  # White daisies
    2: [0, 0, 0]   # Black daisies
}
classified_grid = classify_temperature_grid(
    temperature_grids[-1],
    T_barren, T_white, T_black
)
rgb_grid = np.array([[color_map[cell] for cell in row] for row in classified_grid])
axes[0, 1].imshow(rgb_grid, aspect='auto')
axes[0, 1].set_title('Популация на маргаритките', fontsize=12)

# Температура спрямо слънчева светимост
axes[1, 0].plot(solar_luminosities, temp_with_daisies, label='With Daisies', color='green')
axes[1, 0].plot(solar_luminosities, temp_barren, label='Barren Land', color='brown')
axes[1, 0].set_title('Температура спрямо слънчева светимост', fontsize=12)
axes[1, 0].set_xlabel('слънчева светимост', fontsize=10)
axes[1, 0].set_ylabel('Температура (°C)', fontsize=10)
axes[1, 0].legend()
axes[1, 0].grid(True)

# Слънчева светимост и промяна в Температурата
temp_dist_grid = temperature_grids[-1]
im = axes[1, 1].imshow(temp_dist_grid, cmap='coolwarm', aspect='auto', vmin=0, vmax=50)
axes[1, 1].set_title(f'Слънчева светимост и промяна в Температурата', fontsize=12)
fig.colorbar(im, ax=axes[1, 1], orientation='vertical', label='Temperature [°C]')

plt.tight_layout()
plt.show()
