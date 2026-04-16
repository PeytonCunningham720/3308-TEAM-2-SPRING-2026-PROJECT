"""
database/bird_descriptions.py
Run once to populate the bird_species table with data.
Usage: DB_PASSWORD="" python database/bird_descriptions.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_connection

birds = [
    {
        "common_name": "american_robin",
        "scientific_name": "Turdus migratorius",
        "description": "The American Robin is a migratory songbird with a distinctive orange-red breast and dark back. It is one of the most familiar birds across North America, often seen pulling earthworms from lawns. Robins are known for their cheerful, melodic song which signals the arrival of spring.",
        "ref_image": "bird_images/american_robin.jpg"
    },
    {
        "common_name": "common_loon",
        "scientific_name": "Gavia immer",
        "description": "The Common Loon is a large diving bird known for its haunting, wailing calls that echo across northern lakes. It has striking black and white plumage in summer and is an expert underwater swimmer, diving up to 200 feet to catch fish.",
        "ref_image": "bird_images/common_loon.jpg"
    },
    {
        "common_name": "mourning_dove",
        "scientific_name": "Zenaida macroura",
        "description": "The Mourning Dove is a slender, graceful bird with a soft cooing call that many find mournful and soothing. It is one of the most abundant birds in North America and a common sight at backyard feeders, foraging for seeds on the ground.",
        "ref_image": "bird_images/mourning_dove.jpg"
    },
    {
        "common_name": "pine_warbler",
        "scientific_name": "Setophaga pinus",
        "description": "The Pine Warbler is a small songbird that spends most of its life in pine forests. Males are bright yellow with white wing bars. Its trilling song is a signature sound of southeastern pine woodlands throughout the year.",
        "ref_image": "bird_images/pine_warbler.jpg"
    },
    {
        "common_name": "sandhill_crane",
        "scientific_name": "Antigone canadensis",
        "description": "The Sandhill Crane is a large, long-legged wading bird with a distinctive red forehead and bugling call. One of the oldest living bird species, sandhill cranes are famous for their spectacular migration flocks and elaborate courtship dances.",
        "ref_image": "bird_images/sandhill_crane.jpg"
    },
]

def seed():
    sql = """
        INSERT INTO bird_species (common_name, scientific_name, description, ref_image)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            for bird in birds:
                cur.execute(sql, (
                    bird["common_name"],
                    bird["scientific_name"],
                    bird["description"],
                    bird["ref_image"]
                ))
        conn.commit()
    print(f"[SEEDED] {len(birds)} birds inserted into bird_species.")

if __name__ == "__main__":
    seed()