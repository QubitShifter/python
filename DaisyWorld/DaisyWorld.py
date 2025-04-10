import numpy as np
import matplotlib.pyplot as plt

# Начални параметри
params = {
    #'solar_luminosity_min': 0.3,
    #'solar_luminosity_max': 1.5,
    #'solar_luminosity_step': 0.02,
    #'temp_optimal': 22.5,
    #'temp_white': 15.0,
    #'temp_black': 40.0,
    #'albedo_white': 0.60,
    #'albedo_black': 0.40,
    #'albedo_barren': 0.5,
    #'growth_rate_max': 1.0,


    'solar_luminosity_min': 0.3,
    'solar_luminosity_max': 1.5,
    'solar_luminosity_step': 0.02,
    'temp_optimal': 40.0,  # Set closer to black daisies' preference
    'temp_white': 15.0,
    'temp_black': 40.0,
    'albedo_white': 0.60,
    'albedo_black': 0.35,  # Lower to absorb more heat
    'albedo_barren': 0.5,
    'growth_rate_max': 1.0,
    'initial_area_black': 0.5,  # Dominance of black daisies
    'initial_area_white': 0.2,
    'initial_area_barren': 0.3,
    'mortality_rate': 0.01,  # Lower mortality rate for black daisies




}


# функция за скоростта на растежа
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
temperature_distribution = []


temperature_grids = []

# Симулация
for S in solar_luminosities:
    # Tемпература на пустееща зема, с бели маргаритки и с черни маргаритки
    temp_barren_current = 30 * S * (1 - params['albedo_barren']) ** 0.25
    temp_white_current = 30 * S * (1 - params['albedo_white']) ** 0.25
    temp_black_current = 30 * S * (1 - params['albedo_black']) ** 0.25

    # Скорост на растеж на бели и черни маргаритки
    growth_white = growth_rate(temp_white_current, params['temp_optimal'])
    growth_black = growth_rate(temp_black_current, params['temp_optimal'])

    # Условия за наличи на области с маргаритки
    area_white_current = growth_white if growth_white > 0.1 else 0.0
    area_black_current = growth_black if growth_black > 0.1 else 0.0
    area_barren_current = max(0.0, 1.0 - area_white_current - area_black_current)

    total_area = area_barren_current + area_white_current + area_black_current
    if total_area > 0:
        area_barren_current /= total_area
        area_white_current /= total_area
        area_black_current /= total_area
    else:
        area_barren_current = area_white_current = area_black_current = 0

    # Земна Т при наличие на маргаритки
    planetary_albedo = (area_white_current * params['albedo_white'] +
                        area_black_current * params['albedo_black'] +
                        area_barren_current * params['albedo_barren'])
    temp_with_daisies_current = 30 * S * (1 - planetary_albedo) ** 0.25

    # таблици
    temperature_grid = np.zeros((50, 50))
    colored_grid = np.random.choice(
        [0, 1, 2],  # 0: безплодна земя, 1: бели маргаритки, 2: черни маргаритки
        size=(50, 50),
        p=[area_barren_current, area_white_current, area_black_current]
    )

    for i in range(50):
        for j in range(50):
            if colored_grid[i, j] == 0:  # безплодна земя
                temperature_grid[i, j] = temp_barren_current
            elif colored_grid[i, j] == 1:  # бели маргаритки
                temperature_grid[i, j] = temp_white_current
            elif colored_grid[i, j] == 2:  # черни маргаритки
                temperature_grid[i, j] = temp_black_current

    # записване на резултатите
    area_white.append(area_white_current)
    area_black.append(area_black_current)
    area_barren.append(area_barren_current)
    temp_with_daisies.append(temp_with_daisies_current)
    temp_barren.append(temp_barren_current)
    temperature_distribution.append(temperature_grid)

    # записване на Т
    temperature_grids.append(temperature_grid)


area_white = np.array(area_white)
area_black = np.array(area_black)
area_barren = np.array(area_barren)
temp_with_daisies = np.array(temp_with_daisies)
temp_barren = np.array(temp_barren)

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# % Area vs Solar Luminosity
axes[0, 0].plot(solar_luminosities, area_white, label='Бели маргаритки', color='blue')
axes[0, 0].plot(solar_luminosities, area_black, label='Черни маргаритки', color='black')
axes[0, 0].plot(solar_luminosities, area_barren, label='Пустееща земя', color='brown')
axes[0, 0].set_title('Площ спрямо Слънчева светимост [%]', fontsize=12)
axes[0, 0].set_xlabel('Слънчева светимост', fontsize=10)
axes[0, 0].set_ylabel('Площ [%]', fontsize=10)
axes[0, 0].legend()
axes[0, 0].grid(True)  # Add grid

# Daisy Distribution Visualization
color_map = {0: [139 / 255, 69 / 255, 19 / 255], 1: [1, 1, 1], 2: [0, 0, 0]}  # Barren, White, Black
rgb_grid = np.array([[color_map[cell] for cell in row] for row in colored_grid])
axes[0, 1].imshow(rgb_grid, aspect='auto')
axes[0, 1].set_title('Популация на маргаритките', fontsize=12)

# Temperature vs Solar Luminosity
axes[1, 0].plot(solar_luminosities, temp_with_daisies, label='Бели маргаритки', color='green')
axes[1, 0].plot(solar_luminosities, temp_barren, label='Пустееща земя', color='red')
axes[1, 0].set_title('Температура спрямо Слънчевата светимост', fontsize=12)
axes[1, 0].set_xlabel('Слънчева светимост', fontsize=10)
axes[1, 0].set_ylabel('Температура (°C)', fontsize=10)
axes[1, 0].legend()
axes[1, 0].grid(True)  # Add grid

# разпределение на температурата
temp_dist_grid = temperature_grids[-1]
im = axes[1, 1].imshow(temp_dist_grid, cmap='coolwarm', aspect='auto', vmin=0, vmax=50)
axes[1, 1].set_title(f'Слънчева светимост и промяна в Температурата', fontsize=12)
fig.colorbar(im, ax=axes[1, 1], orientation='vertical', label='Температура [°C]')

plt.tight_layout()
plt.show()
