"""
queries.py — Запросы к графу (1 и 2 уровень).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config import get_collections


def get_city_by_id(city_id):
    """Возвращает информацию о городе по его ID."""
    cities_collection, _ = get_collections()
    return cities_collection.find_one({"_id": city_id})


def get_city_by_name(name):
    """Возвращает информацию о городе по его названию (англ)."""
    cities_collection, _ = get_collections()
    return cities_collection.find_one({"name_en": name})


def get_neighbors(city_id):
    """
    Запрос 1 уровня: возвращает список прямых соседей города.
    
    Args:
        city_id: ID города
        
    Returns:
        list: Список словарей с информацией о соседях и маршрутах
    """
    _, routes_collection = get_collections()
    
    routes = list(routes_collection.find({
        "$or": [
            {"from": city_id},
            {"to": city_id}
        ]
    }))
    
    neighbors = []
    for route in routes:
        neighbor_id = route["to"] if route["from"] == city_id else route["from"]
        city = get_city_by_id(neighbor_id)
        if city:
            neighbors.append({
                "city": city,
                "route": route
            })
    
    return neighbors


def get_neighbors_of_neighbors(city_id):
    """
    Запрос 2 уровня: возвращает города, достижимые с одной пересадкой.
    
    Args:
        city_id: ID города
        
    Returns:
        list: Список словарей с информацией о соседях второго уровня
    """
    first_level = get_neighbors(city_id)
    first_level_ids = [n["city"]["_id"] for n in first_level]
    
    second_level = []
    seen = set([city_id] + first_level_ids)
    
    for neighbor in first_level:
        neighbor_id = neighbor["city"]["_id"]
        for second in get_neighbors(neighbor_id):
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


if __name__ == "__main__":
    # Тестирование для Дубая (ID = 7)
    dubai = get_city_by_name("Dubai")
    
    if not dubai:
        print("Город Dubai не найден в базе данных!")
        print("   Убедитесь, что данные загружены (запустите load_data.py)")
        exit(1)
    
    print(f"Анализ графа для города: {dubai['name']} (ID: {dubai['_id']})")
    
    # Запрос 1 уровня
    print("\n1 уровень (прямые соседи):")
    neighbors = get_neighbors(dubai["_id"])
    
    if not neighbors:
        print("   Нет прямых соседей!")
    else:
        for n in neighbors:
            print(f"  - {n['city']['name']} ({n['city']['country']}) — "
                  f"{n['route']['weight']} км, {n['route']['airline']}")
    
    # Запрос 2 уровня
    print("\n2 уровень (города с одной пересадкой):")
    second_level = get_neighbors_of_neighbors(dubai["_id"])
    
    if not second_level:
        print(" Нет городов с одной пересадкой!")
    else:
        for s in second_level:
            total = s['route1']['weight'] + s['route2']['weight']
            print(f"  - {s['city']['name']} (через {s['via']['name']}) — "
                  f"{s['route1']['weight']} + {s['route2']['weight']} = {total} км")
    
    print(f"Всего прямых соседей: {len(neighbors)}")
    print(f"Всего городов с пересадкой: {len(second_level)}")
