import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# 1. ДАННЫЕ: ГОРОДА (50 вершин)
# =====================================================
cities_data = [
    {"id": 1, "name": "Tokyo", "country": "Japan", "type": "hub", "lat": 35.6762, "lon": 139.6503},
    {"id": 2, "name": "Seoul", "country": "South Korea", "type": "hub", "lat": 37.5665, "lon": 126.9780},
    {"id": 3, "name": "Beijing", "country": "China", "type": "hub", "lat": 39.9042, "lon": 116.4074},
    {"id": 4, "name": "Shanghai", "country": "China", "type": "hub", "lat": 31.2304, "lon": 121.4737},
    {"id": 5, "name": "Hong Kong", "country": "China (SAR)", "type": "hub", "lat": 22.3193, "lon": 114.1694},
    {"id": 6, "name": "Singapore", "country": "Singapore", "type": "hub", "lat": 1.3521, "lon": 103.8198},
    {"id": 7, "name": "Dubai", "country": "UAE", "type": "hub", "lat": 25.2048, "lon": 55.2708},
    {"id": 8, "name": "Doha", "country": "Qatar", "type": "hub", "lat": 25.2854, "lon": 51.5310},
    {"id": 9, "name": "Istanbul", "country": "Turkey", "type": "hub", "lat": 41.0082, "lon": 28.9784},
    {"id": 10, "name": "Delhi", "country": "India", "type": "capital", "lat": 28.6139, "lon": 77.2090},
    {"id": 11, "name": "Mumbai", "country": "India", "type": "hub", "lat": 19.0760, "lon": 72.8777},
    {"id": 12, "name": "Jakarta", "country": "Indonesia", "type": "capital", "lat": -6.2088, "lon": 106.8456},
    {"id": 13, "name": "Bangkok", "country": "Thailand", "type": "hub", "lat": 13.7563, "lon": 100.5018},
    {"id": 14, "name": "Kuala Lumpur", "country": "Malaysia", "type": "hub", "lat": 3.1390, "lon": 101.6869},
    {"id": 15, "name": "Manila", "country": "Philippines", "type": "capital", "lat": 14.5995, "lon": 120.9842},
    {"id": 16, "name": "Karachi", "country": "Pakistan", "type": "major_city", "lat": 24.8607, "lon": 67.0011},
    {"id": 17, "name": "Dhaka", "country": "Bangladesh", "type": "capital", "lat": 23.8103, "lon": 90.4125},
    {"id": 18, "name": "Tehran", "country": "Iran", "type": "capital", "lat": 35.6892, "lon": 51.3890},
    {"id": 19, "name": "Baghdad", "country": "Iraq", "type": "capital", "lat": 33.3152, "lon": 44.3661},
    {"id": 20, "name": "Riyadh", "country": "Saudi Arabia", "type": "capital", "lat": 24.7136, "lon": 46.6753},
    {"id": 21, "name": "Abu Dhabi", "country": "UAE", "type": "capital", "lat": 24.4539, "lon": 54.3773},
    {"id": 22, "name": "Muscat", "country": "Oman", "type": "capital", "lat": 23.5880, "lon": 58.3829},
    {"id": 23, "name": "Tashkent", "country": "Uzbekistan", "type": "capital", "lat": 41.2995, "lon": 69.2401},
    {"id": 24, "name": "Almaty", "country": "Kazakhstan", "type": "major_city", "lat": 43.2220, "lon": 76.8512},
    {"id": 25, "name": "Astana", "country": "Kazakhstan", "type": "capital", "lat": 51.1694, "lon": 71.4491},
    {"id": 26, "name": "Taipei", "country": "Taiwan", "type": "capital", "lat": 25.0330, "lon": 121.5654},
    {"id": 27, "name": "Osaka", "country": "Japan", "type": "major_city", "lat": 34.6937, "lon": 135.5023},
    {"id": 28, "name": "Nagoya", "country": "Japan", "type": "major_city", "lat": 35.1815, "lon": 136.9066},
    {"id": 29, "name": "Guangzhou", "country": "China", "type": "major_city", "lat": 23.1291, "lon": 113.2644},
    {"id": 30, "name": "Shenzhen", "country": "China", "type": "major_city", "lat": 22.5431, "lon": 114.0579},
    {"id": 31, "name": "Chengdu", "country": "China", "type": "major_city", "lat": 30.5728, "lon": 104.0668},
    {"id": 32, "name": "Chongqing", "country": "China", "type": "major_city", "lat": 29.5630, "lon": 106.5516},
    {"id": 33, "name": "Bangalore", "country": "India", "type": "major_city", "lat": 12.9716, "lon": 77.5946},
    {"id": 34, "name": "Chennai", "country": "India", "type": "major_city", "lat": 13.0827, "lon": 80.2707},
    {"id": 35, "name": "Hyderabad", "country": "India", "type": "major_city", "lat": 17.3850, "lon": 78.4867},
    {"id": 36, "name": "Lahore", "country": "Pakistan", "type": "major_city", "lat": 31.5204, "lon": 74.3587},
    {"id": 37, "name": "Hanoi", "country": "Vietnam", "type": "capital", "lat": 21.0278, "lon": 105.8342},
    {"id": 38, "name": "Ho Chi Minh", "country": "Vietnam", "type": "major_city", "lat": 10.8231, "lon": 106.6297},
    {"id": 39, "name": "Yangon", "country": "Myanmar", "type": "capital", "lat": 16.8661, "lon": 96.1951},
    {"id": 40, "name": "Busan", "country": "South Korea", "type": "major_city", "lat": 35.1796, "lon": 129.0756},
    {"id": 41, "name": "Colombo", "country": "Sri Lanka", "type": "capital", "lat": 6.9271, "lon": 79.8612},
    {"id": 42, "name": "Kathmandu", "country": "Nepal", "type": "capital", "lat": 27.7172, "lon": 85.3240},
    {"id": 43, "name": "Islamabad", "country": "Pakistan", "type": "capital", "lat": 33.6844, "lon": 73.0479},
    {"id": 44, "name": "Kuwait City", "country": "Kuwait", "type": "capital", "lat": 29.3759, "lon": 47.9774},
    {"id": 45, "name": "Manama", "country": "Bahrain", "type": "capital", "lat": 26.2285, "lon": 50.5860},
    {"id": 46, "name": "Amman", "country": "Jordan", "type": "capital", "lat": 31.9454, "lon": 35.9284},
    {"id": 47, "name": "Beirut", "country": "Lebanon", "type": "capital", "lat": 33.8938, "lon": 35.5018},
    {"id": 48, "name": "Damascus", "country": "Syria", "type": "capital", "lat": 33.5138, "lon": 36.2765},
    {"id": 49, "name": "Erbil", "country": "Iraq", "type": "major_city", "lat": 36.1825, "lon": 44.0085},
    {"id": 50, "name": "Shiraz", "country": "Iran", "type": "major_city", "lat": 29.5918, "lon": 52.5837}
]

# =====================================================
# 2. ДАННЫЕ: МАРШРУТЫ (87 рёбер)
# =====================================================
routes_data = [
    # От Токио (1)
    (1, 2, 1150), (1, 3, 2100), (1, 4, 1750), (1, 5, 2900), (1, 27, 400), (1, 28, 260),
    # От Сеула (2)
    (2, 3, 950), (2, 4, 800), (2, 5, 2050), (2, 26, 1450), (2, 40, 320),
    # От Пекина (3)
    (3, 4, 1050), (3, 5, 1950), (3, 29, 1900), (3, 31, 1700), (3, 32, 1450), (3, 26, 1700),
    # От Шанхая (4)
    (4, 5, 1250), (4, 29, 1200), (4, 30, 1200), (4, 26, 675),
    # От Гонконга (5)
    (5, 6, 2550), (5, 13, 1700), (5, 29, 1100), (5, 30, 950), (5, 26, 805),
    # От Сингапура (6)
    (6, 13, 1850), (6, 14, 300), (6, 15, 2400), (6, 12, 900), (6, 7, 5850),
    # От Дубая (7)
    (7, 8, 380), (7, 9, 3000), (7, 11, 2100), (7, 21, 280), (7, 20, 870), (7, 44, 850), (7, 45, 485),
    # От Дохи (8)
    (8, 7, 380), (8, 11, 2050), (8, 20, 1550), (8, 44, 1400), (8, 46, 1550),
    # От Стамбула (9)
    (9, 18, 2200), (9, 19, 1400), (9, 46, 800), (9, 47, 900), (9, 48, 700), (9, 44, 2000),
    # От Дели (10)
    (10, 11, 1150), (10, 33, 1750), (10, 34, 1750), (10, 35, 1250), (10, 43, 650),
    # От Мумбаи (11)
    (11, 33, 850), (11, 34, 1000), (11, 41, 1500), (11, 16, 1150),
    # От Джакарты (12)
    (12, 6, 900), (12, 38, 2000),
    # От Бангкока (13)
    (13, 6, 1850), (13, 14, 1200), (13, 37, 1100), (13, 38, 700), (13, 39, 600), (13, 17, 1400),
    # От Куала-Лумпур (14)
    (14, 6, 300), (14, 15, 2500), (14, 12, 1100),
    # От Манилы (15)
    (15, 5, 1150), (15, 26, 1170), (15, 40, 2600),
    # От Карачи (16)
    (16, 7, 1200), (16, 10, 1150), (16, 43, 1200),
    # От Дакки (17)
    (17, 6, 2900), (17, 13, 1400), (17, 10, 1450),
    # От Тегерана (18)
    (18, 9, 2200), (18, 19, 1000), (18, 49, 800), (18, 50, 750), (18, 46, 1550),
    # От Багдада (19)
    (19, 9, 1400), (19, 46, 1050), (19, 48, 700),
    # От Эр-Рияда (20)
    (20, 7, 870), (20, 8, 1550), (20, 44, 600), (20, 45, 400),
    # От Абу-Даби (21)
    (21, 7, 280), (21, 11, 1900), (21, 44, 700), (21, 45, 450),
    # От Маската (22)
    (22, 7, 350), (22, 44, 1400),
    # От Ташкента (23)
    (23, 9, 3200), (23, 24, 700), (23, 25, 850), (23, 10, 1700),
    # От Алматы (24)
    (24, 9, 3900), (24, 23, 700), (24, 25, 950), (24, 3, 3400),
    # От Астаны (25)
    (25, 9, 3700), (25, 24, 950), (25, 23, 850), (25, 3, 3700),
    # От Тайбэя (26)
    (26, 2, 1450), (26, 3, 1700), (26, 4, 675), (26, 5, 805), (26, 15, 1170), (26, 40, 1550),
    # От Осаки (27)
    (27, 1, 400), (27, 4, 1350),
    # От Нагои (28)
    (28, 1, 260), (28, 3, 1900),
    # От Гуанчжоу (29)
    (29, 3, 1900), (29, 4, 1200), (29, 5, 1100), (29, 13, 1600),
    # От Шэньчжэня (30)
    (30, 4, 1200), (30, 5, 950), (30, 13, 1600),
    # От Чэнду (31)
    (31, 3, 1700), (31, 10, 2300), (31, 13, 1900),
    # От Чунцина (32)
    (32, 3, 1450), (32, 10, 2700),
    # От Бангалора (33)
    (33, 10, 1750), (33, 11, 850), (33, 41, 1050),
    # От Ченная (34)
    (34, 10, 1750), (34, 11, 1000), (34, 6, 2900),
    # От Хайдарабада (35)
    (35, 10, 1250), (35, 11, 650),
    # От Лахора (36)
    (36, 7, 1950), (36, 10, 450), (36, 43, 250),
    # От Ханоя (37)
    (37, 13, 1100), (37, 6, 2200), (37, 5, 850),
    # От Хошимина (38)
    (38, 13, 700), (38, 12, 2000), (38, 6, 1950),
    # От Янгона (39)
    (39, 13, 600), (39, 6, 2200),
    # От Пусана (40)
    (40, 2, 320), (40, 26, 1550), (40, 15, 2600),
    # От Коломбо (41)
    (41, 11, 1500), (41, 33, 1050), (41, 6, 2700),
    # От Катманду (42)
    (42, 10, 800), (42, 17, 800),
    # От Исламабада (43)
    (43, 10, 650), (43, 16, 1200), (43, 36, 250),
    # От Кувейта (44)
    (44, 7, 850), (44, 8, 1400), (44, 20, 600), (44, 21, 700), (44, 22, 1400),
    # От Манамы (45)
    (45, 7, 485), (45, 8, 700), (45, 20, 400), (45, 21, 450),
    # От Аммана (46)
    (46, 8, 1550), (46, 9, 800), (46, 18, 1550), (46, 19, 1050), (46, 47, 220),
    # От Бейрута (47)
    (47, 9, 900), (47, 46, 220), (47, 48, 110),
    # От Дамаска (48)
    (48, 9, 700), (48, 19, 700), (48, 47, 110),
    # От Эрбиля (49)
    (49, 18, 800), (49, 9, 1300),
    # От Шираза (50)
    (50, 18, 750), (50, 7, 700)
]

# =====================================================
# 3. ПОСТРОЕНИЕ ГРАФА
# =====================================================

# Создаём граф
G = nx.Graph()

# Добавляем вершины с атрибутами
for city in cities_data:
    G.add_node(city["id"], 
               name=city["name"], 
               country=city["country"], 
               type=city["type"],
               lat=city["lat"], 
               lon=city["lon"])

# Добавляем рёбра с весом
for from_id, to_id, weight in routes_data:
    G.add_edge(from_id, to_id, weight=weight)

# =====================================================
# 4. НАСТРОЙКИ ВИЗУАЛИЗАЦИИ
# =====================================================

# Цвета для разных типов городов
color_map = {
    "hub": "#FF4444",       # Красный для хабов
    "capital": "#4488FF",   # Синий для столиц
    "major_city": "#44BB44" # Зелёный для крупных городов
}

# Получаем цвета для каждой вершины
node_colors = [color_map[G.nodes[node]["type"]] for node in G.nodes()]

# Получаем названия городов для подписей
labels = {node: G.nodes[node]["name"] for node in G.nodes()}

# Размер узлов в зависимости от типа
node_sizes = []
for node in G.nodes():
    if G.nodes[node]["type"] == "hub":
        node_sizes.append(1200)      # Хабы большие
    elif G.nodes[node]["type"] == "capital":
        node_sizes.append(800)       # Столицы средние
    else:
        node_sizes.append(500)       # Остальные маленькие

# =====================================================
# 5. РИСОВАНИЕ ГРАФА
# =====================================================

plt.figure(figsize=(20, 16))

# Позиционирование узлов по координатам (для реалистичной карты)
pos = {node: (G.nodes[node]["lon"], G.nodes[node]["lat"]) for node in G.nodes()}

# Рисуем граф
nx.draw_networkx_nodes(G, pos, 
                       node_color=node_colors, 
                       node_size=node_sizes,
                       alpha=0.9,
                       edgecolors='black',
                       linewidths=1.5)

# Рисуем рёбра с прозрачностью
nx.draw_networkx_edges(G, pos, 
                       alpha=0.3, 
                       edge_color='gray',
                       width=0.8)

# Подписи городов
nx.draw_networkx_labels(G, pos, labels, 
                        font_size=9, 
                        font_weight='bold',
                        bbox=dict(boxstyle="round,pad=0.3", 
                                 facecolor="white", 
                                 edgecolor="none", 
                                 alpha=0.8))

# Заголовок и настройки
plt.title("Граф азиатских авиаперелётов (50 городов, 87 маршрутов)", 
          fontsize=20, fontweight='bold', pad=20)
plt.xlabel("Долгота", fontsize=12)
plt.ylabel("Широта", fontsize=12)
plt.grid(True, alpha=0.3)

# Легенда
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#FF4444', label='Хаб (9 городов)', edgecolor='black'),
    Patch(facecolor='#4488FF', label='Столица (26 городов)', edgecolor='black'),
    Patch(facecolor='#44BB44', label='Крупный город (15 городов)', edgecolor='black')
]
plt.legend(handles=legend_elements, loc='upper left', fontsize=12)

plt.tight_layout()
plt.savefig('asia_flights_graph.png', dpi=300, bbox_inches='tight')
plt.show()

# =====================================================
# 6. СТАТИСТИКА ГРАФА
# =====================================================
print("=" * 60)
print("📊 ХАРАКТЕРИСТИКИ ГРАФА")
print("=" * 60)
print(f"Количество вершин: {G.number_of_nodes()}")
print(f"Количество рёбер: {G.number_of_edges()}")
print(f"Средняя степень: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")

# Степени вершин
degrees = dict(G.degree())
hubs = [node for node, deg in degrees.items() if deg >= 6]
print(f"Хабы (степень >= 6): {len(hubs)}")
for hub in hubs:
    print(f"  - {G.nodes[hub]['name']}: {degrees[hub]} связей")

# Диаметр графа (если граф связный)
if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f"Диаметр графа: {diameter}")
else:
    print("Граф не является связным, диаметр не определён")

# Подсчёт компонент связности
components = list(nx.connected_components(G))
print(f"Количество компонент связности: {len(components)}")