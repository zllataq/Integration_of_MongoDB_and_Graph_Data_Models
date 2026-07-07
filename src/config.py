"""
config.py — Подключение к MongoDB.
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "practice_graph")


def get_database():
    """Возвращает подключение к базе данных MongoDB."""
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        return client[DATABASE_NAME]
    except Exception as e:
        print(f"Ошибка подключения к MongoDB: {e}")
        raise


def get_collections():
    """Возвращает коллекции cities и routes."""
    db = get_database()
    return db["cities"], db["routes"]


if __name__ == "__main__":
    try:
        db = get_database()
        print(f"Подключение к MongoDB установлено!")
        print(f"   База данных: {DATABASE_NAME}")
        print(f"   Коллекции: {db.list_collection_names()}")
    except Exception as e:
        print(f" Ошибка: {e}")