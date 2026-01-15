LEVEL_CONFIG = {
    "surface_goal": {"child_type": "attack_vector", "min": 4, "max": 7},
    "attack_vector": {"child_type": "method", "min": 2, "max": 4},
    "method": {"child_type": "technique", "min": 2, "max": 4},
    "technique": {"child_type": "technique", "min": 1, "max": 3},
}
