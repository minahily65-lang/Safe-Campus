# config.py

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"

DATABASE_NAME = "safe_campus"

client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]

users_collection = db["users"]

alerts_collection = db["sos_alerts"]

history_collection = db["emergency_history"]