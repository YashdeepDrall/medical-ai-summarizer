from pymongo import MongoClient
from backend.config import MONGODB_URI, DATABASE_NAME

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]


def init_db():
    
    collections = db.list_collection_names()

    if "patients" not in collections:
        db.create_collection("patients")

    if "reports" not in collections:
        db.create_collection("reports")

    if "summaries" not in collections:
        db.create_collection("summaries")


patients_collection = db["patients"]
reports_collection = db["reports"]
summaries_collection = db["summaries"]