"""
load_data.py - Загрузка данных из JSON-файлов в MongoDB.
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.config import get_collections


def load_data():
    """Загружает данные из JSON-файлов в MongoDB."""
    try:
        cities_collection, routes_collection = get_collections()
        
        base_dir = os.path.dirname(os.path.dirname(__file__))
        cities_file = os.path.join(base_dir, "data", "cities.json")
        routes_file = os.path.join(base_dir, "data", "routes.json")
        
        if not os.path.exists(cities_file):
            print(f"Файл не найден: {cities_file}")
            print("   Создайте файл data/cities.json с данными о городах.")
            return False
            
        if not os.path.exists(routes_file):
            print(f"Файл не найден: {routes_file}")
            print("   Создайте файл data/routes.json с данными о маршрутах.")
            return False
        
        print("Очистка существующих коллекций...")
        cities_collection.delete_many({})
        routes_collection.delete_many({})
        
        print(f"Загрузка городов из {cities_file}...")
        with open(cities_file, 'r', encoding='utf-8') as f:
            cities = json.load(f)
        
        if not cities:
            print("Файл cities.json пуст!")
            return False
            
        cities_collection.insert_many(cities)
        print(f"   Загружено {len(cities)} городов")
        
        print(f"Загрузка маршрутов из {routes_file}...")
        with open(routes_file, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        
        if not routes:
            print("Файл routes.json пуст!")
            return False
            
        routes_collection.insert_many(routes)
        print(f"   Загружено {len(routes)} маршрутов")
        
        print("Создание индексов...")
        cities_collection.create_index("name")
        cities_collection.create_index("type")
        routes_collection.create_index("from")
        routes_collection.create_index("to")
        routes_collection.create_index([("from", 1), ("to", 1)])
        routes_collection.create_index("weight")
        print("  Индексы созданы!")
        
        print("Данные успешно загружены!")
        print(f"   Городов: {cities_collection.count_documents({})}")
        print(f"   Маршрутов: {routes_collection.count_documents({})}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"Ошибка в JSON-файле: {e}")
        print("   Проверьте синтаксис JSON (кавычки, запятые).")
        return False
        
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        return False


def show_sample_data():
    """Показывает пример данных из коллекций."""
    try:
        cities_collection, routes_collection = get_collections()
        
        print("\nПример данных:")
        
        city = cities_collection.find_one()
        if city:
            print("Пример города:")
            print(f"   {city}")
        
        route = routes_collection.find_one()
        if route:
            print("\nПример маршрута:")
            print(f"   {route}")
            
    except Exception as e:
        print(f" Ошибка при показе данных: {e}")


if __name__ == "__main__":
    success = load_data()
    
    if success:
        show_sample_data()