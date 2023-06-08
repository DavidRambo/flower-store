"""Adds to, removes from, and queries the elasticsearch index.

Adapted from Miguel Grinberg's Flask Mega-Tutorial, with changes made to
query_index.

Each function first checks whether the current Flask application has
enabled elasticsearch.

: Args :
    index : name of the Elasticsearch index
    model : the SQLAlchemy model providing the content for the index
"""
from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query):
    if not current_app.elasticsearch:
        return
    search = current_app.elasticsearch.search(
        index=index,
        body={"query": {"match": {"name": {"query": query, "fuzziness": "AUTO"}}}},
    )
    ids = [int(hit["_id"]) for hit in search["hits"]["hits"]]
    return ids, search["hits"]["total"]["value"]
