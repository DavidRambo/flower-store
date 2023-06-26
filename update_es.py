"""Updates the `flower` index in the SearchBox elasticsearch connection."""
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

from elasticsearch import Elasticsearch
from supabase import create_client, Client

load_dotenv()


def setup_supabase() -> Client:
    url_db: str = os.environ.get("SUPABASE_URL")
    key_db: str = os.environ.get("SUPABASE_KEY")

    supa: Client = create_client(url_db, key_db)

    return supa


def setup_elastic() -> Elasticsearch:
    url_es: str = urlparse(os.environ.get("ELASTICSEARCH_URL"))
    key_es: str = os.environ.get("ELASTICSEARCH_KEY")
    es = Elasticsearch(
        "https://" + url_es.hostname + ":443",
        basic_auth=(url_es.username, url_es.password),
    )

    return es


# ignore 400 caused by IndexAlreadyExistsException
# es.indices.create(index="flower", ignore=400)


def create_test_entry(es: Elasticsearch) -> None:
    # Create flower name entry.
    doc = {
        "name": "test",
    }
    res = es.index(index="flower", id=1, document=doc)
    print(res["created"])


# def pop_flowers():
#     """Populates the database with Flowers for the sake of development."""

#     # Delete existing data.
#     data = supa.table("flower").select("id").execute().data

#     for idx, _ in enumerate(data):
#         supa.table("flower").delete().eq("id", data[idx]["id"]).execute()

#     flowers = [
#         "A-Peeling",
#         "Bride To Be",
#         "Café au Lait",
#         "Cheers",
#         "Daddy's Girl",
#         "Diva",
#         "Fluffles",
#         "Foxy Lady",
#         "Ice Tea",
#         "KA's Bella Luna",
#         "KA's Blood Orange",
#         "KA's Boho Peach",
#         "KA's Cloud",
#         "KA's Mocha Jake",
#         "KA's Mocha Maya",
#         "L'Ancress",
#         "Lovebug",
#         "Mai Tai",
#         "Maki",
#         "Marshmallow",
#         "Maui",
#         "Moonstruck",
#         "Ranunculus",
#         "Snapdragon",
#         "Straw flower",
#         "Tootles",
#     ]
#     shuffle(flowers)

#     for flower in flowers:
#         if flower == "Straw flower":
#             supa.table("flower").insert(
#                 {
#                     "name": flower,
#                     "stock": randint(0, 10),
#                     "image_file": "strawflower_edb8f2b8dc93.png",
#                     "price": float(randint(5, 35)),
#                 }
#             ).execute()
#         elif flower == "Ranunculus":
#             supa.table("flower").insert(
#                 {
#                     "name": flower,
#                     "stock": randint(0, 10),
#                     "image_file": "ranunculus_fc5fbcc0f.jpg",
#                     "price": float(randint(5, 35)),
#                 }
#             ).execute()
#         else:
#             supa.table("flower").insert(
#                 {
#                     "name": flower,
#                     "stock": randint(0, 10),
#                     "image_file": "default.png",
#                     "price": float(randint(5, 35)),
#                 }
#             ).execute()


# if __name__ == "__main__":
#     raise SystemExit(pop_flowers())
