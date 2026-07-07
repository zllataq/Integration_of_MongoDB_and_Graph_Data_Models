import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "practice_graph")

def get_database():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    return db

def get_collections():
    db = get_database()
    return db["cities"], db["routes"]