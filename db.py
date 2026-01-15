from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set")

client = MongoClient(MONGO_URI)
db = client["attack_tree_db"]
trees = db["atomic_attack_trees"]


def get_tree(surface_goal: str):
    doc = trees.find_one({"surface_goal": surface_goal})
    return doc["tree"] if doc else None


def get_all_surface_goals():
    return sorted(trees.distinct("surface_goal"))


def save_tree(surface_goal: str, tree_json: dict):
    trees.update_one(
        {"surface_goal": surface_goal},
        {
            "$set": {
                "tree": tree_json,
                "updated_at": datetime.utcnow()
            },
            "$setOnInsert": {
                "surface_goal": surface_goal,
                "created_at": datetime.utcnow()
            }
        },
        upsert=True
    )
