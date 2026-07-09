"""
performance_test.py — Тестирование производительности.
Сравнение скорости запросов в MongoDB и в Python-структурах.
"""

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config import get_collections
from src.queries import get_city_by_name, get_neighbors, get_neighbors_of_neighbors



# 1. Подготовка данных в Python (без MongoDB)
def load_data_from_json():
    """Загружает данные из JSON-файлов в Python-структуры."""
    import json
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    cities_file = os.path.join(base_dir, "data", "cities.json")
    routes_file = os.path.join(base_dir, "data", "routes.json")
    
    with open(cities_file, 'r', encoding='utf-8') as f:
        cities_data = json.load(f)
    
    with open(routes_file, 'r', encoding='utf-8') as f:
        routes_data = json.load(f)
    
    # Словарь городов: city_id -> {name, country, type}
    cities_dict = {}
    for city in cities_data:
        cities_dict[city["_id"]] = {
            "name": city["name"],
            "name_en": city["name_en"],
            "country": city["country"],
            "type": city["type"]
        }
    
    # Словарь соседей: city_id -> [neighbor_id, ...]
    neighbors_dict = {}
    for route in routes_data:
        from_id = route["from"]
        to_id = route["to"]
        
        if from_id not in neighbors_dict:
            neighbors_dict[from_id] = []
        if to_id not in neighbors_dict:
            neighbors_dict[to_id] = []
        
        if to_id not in neighbors_dict[from_id]:
            neighbors_dict[from_id].append(to_id)
        if from_id not in neighbors_dict[to_id]:
            neighbors_dict[to_id].append(from_id)
    
    # Словарь маршрутов: (from, to) -> {weight, airline}
    routes_dict = {}
    for route in routes_data:
        key = (route["from"], route["to"])
        routes_dict[key] = {
            "weight": route["weight"],
            "airline": route["airline"]
        }
        key_rev = (route["to"], route["from"])
        if key_rev not in routes_dict:
            routes_dict[key_rev] = {
                "weight": route["weight"],
                "airline": route["airline"]
            }
    
    return cities_dict, neighbors_dict, routes_dict


# 2. Запросы на Python-структурах (без MongoDB)
def get_neighbors_python(city_id, neighbors_dict, cities_dict, routes_dict):
    """Запрос 1 уровня на Python-структурах."""
    neighbors = []
    if city_id not in neighbors_dict:
        return neighbors
    
    for neighbor_id in neighbors_dict[city_id]:
        city = cities_dict.get(neighbor_id)
        if city:
            city_with_id = city.copy()
            city_with_id["_id"] = neighbor_id
            route_key = (city_id, neighbor_id)
            route = routes_dict.get(route_key, {})
            neighbors.append({
                "city": city_with_id,
                "route": route
            })
    
    return neighbors


def get_neighbors_of_neighbors_python(city_id, neighbors_dict, cities_dict, routes_dict):
    """Запрос 2 уровня на Python-структурах."""
    first_level = get_neighbors_python(city_id, neighbors_dict, cities_dict, routes_dict)
    first_level_ids = [n["city"]["_id"] for n in first_level]
    
    second_level = []
    seen = set([city_id] + first_level_ids)
    
    for neighbor in first_level:
        neighbor_id = neighbor["city"]["_id"]
        for second in get_neighbors_python(neighbor_id, neighbors_dict, cities_dict, routes_dict):
            second_id = second["city"]["_id"]
            if second_id not in seen:
                seen.add(second_id)
                second_level.append({
                    "city": second["city"],
                    "via": neighbor["city"],
                    "route1": neighbor["route"],
                    "route2": second["route"]
                })
    
    return second_level


# 3. Тестирование производительности
def run_performance_test():
    """Запускает тестирование производительности."""
    
    print("ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ\n")    
    # Загрузка данных в Python
    print("\n Загрузка данных в Python-структуры")
    cities_dict, neighbors_dict, routes_dict = load_data_from_json()
    print(f"   Городов: {len(cities_dict)}")
    print(f"   Городов с соседями: {len(neighbors_dict)}")
    print(f"   Маршрутов (включая обратные): {len(routes_dict)}")
    
    # Подготовка к тестам
    dubai_id = None
    for cid, info in cities_dict.items():
        if info["name_en"] == "Dubai":
            dubai_id = cid
            break
    
    if dubai_id is None:
        print("Город Dubai не найден в Python-данных!")
        return
    
    print(f"\nТестирование для города: {cities_dict[dubai_id]['name']} (ID: {dubai_id})")
    
    # Инициализация переменных (на случай ошибки)
    time_mongo_1 = 0
    time_python_1 = 0
    time_mongo_2 = 0
    time_python_2 = 0
    neighbors_mongo = []
    neighbors_python = []
    second_level_mongo = []
    second_level_python = []
    
    #тест 1: Запрос 1 уровня (прямые соседи)
    print("\nТест 1: Запрос 1 уровня (прямые соседи)\n")
    
    try:
        # MongoDB
        print("\nMongoDB:")
        start = time.time()
        neighbors_mongo = get_neighbors(dubai_id)
        end = time.time()
        time_mongo_1 = end - start
        print(f"   Время: {time_mongo_1:.6f} сек")
        print(f"   Найдено соседей: {len(neighbors_mongo)}")
    except Exception as e:
        print(f" Ошибка MongoDB: {e}")
    
    try:
        # Python
        print("\nPython (без MongoDB):")
        start = time.time()
        neighbors_python = get_neighbors_python(dubai_id, neighbors_dict, cities_dict, routes_dict)
        end = time.time()
        time_python_1 = end - start
        print(f"   Время: {time_python_1:.6f} сек")
        print(f"   Найдено соседей: {len(neighbors_python)}")
    except Exception as e:
        print(f" Ошибка Python: {e}")
    
    #Тест 2: Запрос 2 уровня (соседи соседей)
    print("Тест 2: Запрос 2 уровня (соседи соседей)\n")
    
    try:
        # MongoDB
        print("\nMongoDB:")
        start = time.time()
        second_level_mongo = get_neighbors_of_neighbors(dubai_id)
        end = time.time()
        time_mongo_2 = end - start
        print(f"   Время: {time_mongo_2:.6f} сек")
        print(f"   Найдено городов с пересадкой: {len(second_level_mongo)}")
    except Exception as e:
        print(f" Ошибка MongoDB: {e}")
    
    try:
        # Python
        print("\nPython (без MongoDB):")
        start = time.time()
        second_level_python = get_neighbors_of_neighbors_python(dubai_id, neighbors_dict, cities_dict, routes_dict)
        end = time.time()
        time_python_2 = end - start
        print(f"   Время: {time_python_2:.6f} сек")
        print(f"   Найдено городов с пересадкой: {len(second_level_python)}")
    except Exception as e:
        print(f"  Ошибка Python: {e}")
    
    # Результаты

    print("\nТаблица результатов\n")

    print("ЗАПРОС 1 УРОВНЯ (прямые соседи)\n")
    print(f"  MongoDB:                {time_mongo_1:.6f} сек")
    print(f"  Python (без MongoDB):   {time_python_1:.6f} сек")
    if time_python_1 > 0:
        print(f"  Отношение MongoDB / Python:  {time_mongo_1/time_python_1:.2f}x")
    else:
        print("  Отношение MongoDB / Python:  N/A (Python занял 0 сек)")
    print(f"  Найдено соседей (MongoDB):  {len(neighbors_mongo)}")
    print(f"  Найдено соседей (Python):   {len(neighbors_python)}")
    
    print("\n" + "-" * 70)
    print("ЗАПРОС 2 УРОВНЯ (соседи соседей)")
    print("-" * 70)
    print(f"  MongoDB:                {time_mongo_2:.6f} сек")
    print(f"  Python (без MongoDB):   {time_python_2:.6f} сек")
    if time_python_2 > 0:
        print(f"  Отношение MongoDB / Python:  {time_mongo_2/time_python_2:.2f}x")
    else:
        print("  Отношение MongoDB / Python:  N/A (Python занял 0 сек)")
    print(f"  Найдено городов с пересадкой (MongoDB): {len(second_level_mongo)}")
    print(f"  Найдено городов с пересадкой (Python):  {len(second_level_python)}")


if __name__ == "__main__":
    run_performance_test()