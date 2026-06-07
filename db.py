from pymongo import MongoClient
from datetime import datetime
import os

# 🔐 Read from environment variable (Docker/Render) or Streamlit secrets (fallback)
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    try:
        import streamlit as st
        MONGO_URI = st.secrets.get("MONGO_URI")
    except Exception:
        pass

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set. Set it as an environment variable or in .streamlit/secrets.toml")

DB_NAME = "attack_tree_db"
COLLECTION = "atomic_attack_tree"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
trees = db[COLLECTION]


def get_tree(surface_goal: str):
    # Sort by created_at descending to get the newest version
    return trees.find_one(
        {"surface_goal": surface_goal},
        sort=[("created_at", -1)]
    )


def save_tree(surface_goal: str, tree_json: dict):
    print("🔥 Saving/Updating tree in MongoDB for surface goal:", surface_goal)

    # Use update_one with upsert=True to overwrite the specific goal
    result = trees.update_one(
        {"surface_goal": surface_goal},
        {
            "$set": {
                "tree": tree_json,
                "created_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    if result.upserted_id:
        print("✅ Created new document ID:", result.upserted_id)
    else:
        print("✅ Updated existing document")

   
