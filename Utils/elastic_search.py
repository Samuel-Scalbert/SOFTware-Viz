from elasticsearch import Elasticsearch

def sync_to_elasticsearch(db):
    # Elasticsearch feeding
    es = Elasticsearch('http://localhost:9200')
    # SOFTWARE ---------------------------------
    collection_software = db['softwares']
    # Delete index if exists
    if es.indices.exists(index="softwares"):
        es.indices.delete(index="softwares")
    # Create index with lowercase normalizer mapping
    index_body = {
        "settings": {
            "analysis": {
                "normalizer": {
                    "lowercase_normalizer": {
                        "type": "custom",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "lowercase": {
                            "type": "keyword",
                            "normalizer": "lowercase_normalizer"
                        }
                    }
                }
            }
        }
    }
    es.indices.create(index="softwares", body=index_body)
    # Fetch distinct software names from ArangoDB
    cursor = db.AQLQuery('FOR software IN softwares RETURN DISTINCT {name : software.software_name.normalizedForm}',
                         rawResults=True)
    list_software_names = list(cursor)
    # Index each document into Elasticsearch
    for doc in list_software_names:
        es.index(index='softwares', document=doc)

    # DOCUMENT -----------------------------
    # Delete if index exists
    if es.indices.exists(index="titles"):
        es.indices.delete(index="titles")
    # Create index with n-gram analyzer for partial matching
    index_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 4,
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "search_analyzer": "standard"
                },
                "doc_id": {
                    "type": "keyword"
                }
            }
        }
    }
    es.indices.create(index="titles", body=index_body)
    # Fetch distinct titles and ids from ArangoDB
    cursor = db.AQLQuery('FOR doc IN documents RETURN DISTINCT { title: doc.title, hal_id: doc.file_hal_id}',
                         rawResults=True)
    list_titles = list(cursor)
    # Index each document into Elasticsearch
    for doc in list_titles:
        es.index(index="titles", document={"title": doc['title'], "doc_id": doc['hal_id']})

    # AUTHOR ---------------------------------
    # Delete if exists
    if es.indices.exists(index="authors"):
        es.indices.delete(index="authors")

    index_body = {
        "settings": {
            "analysis": {
                "normalizer": {
                    "lowercase_normalizer": {
                        "type": "custom",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "first_name": {
                    "type": "keyword",
                    "normalizer": "lowercase_normalizer"
                },
                "last_name": {
                    "type": "keyword",
                    "normalizer": "lowercase_normalizer"
                },
                "author_id": {
                    "type": "keyword"
                }
            }
        }
    }
    es.indices.create(index="authors", body=index_body)
    # Fetch distinct authors from ArangoDB
    cursor = db.AQLQuery('''
           FOR author IN authors
           RETURN DISTINCT {
               first_name: author.name.forename,
               last_name: author.name.surname,
               author_id: author.id.halauthorid
           }
       ''', rawResults=True)
    authors_list = list(cursor)
    # Index authors into Elasticsearch
    for author in authors_list:
        es.index(index='authors', document={
            'first_name': author['first_name'],
            'last_name': author['last_name'],
            'author_id': author['author_id']
        })

    # STRUCTURE ---------------------------------------------
    # Delete index if exists
    if es.indices.exists(index="structures"):
        es.indices.delete(index="structures")

    index_body = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "tokenizer": "ngram_tokenizer",
                        "filter": ["lowercase"]
                    },
                    "lowercase_keyword_analyzer": {
                        "tokenizer": "keyword",
                        "filter": ["lowercase"]
                    }
                },
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 2,
                        "max_gram": 3,
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                },
                "normalizer": {
                    "lowercase_normalizer": {
                        "type": "custom",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "structure": {
                    "type": "text",
                    "analyzer": "ngram_analyzer",
                    "search_analyzer": "ngram_analyzer"
                },
                "struct_acronym": {
                    "type": "keyword",
                    "normalizer": "lowercase_normalizer"
                },
                "structure_id": {
                    "type": "keyword"
                }
            }
        }
    }

    es.indices.create(index="structures", body=index_body)

    # Fetch distinct structures and acronyms from ArangoDB
    cursor = db.AQLQuery('''
           FOR struc IN structures
           RETURN DISTINCT {
               struct_title: struc.name,
               struct_acronym: struc.acronym,
               struct_id: struc.id_haureal
           }
       ''', rawResults=True)

    list_structures = list(cursor)

    # Index each structure document
    for struc in list_structures:
        es.index(
            index="structures",
            document={
                "structure": struc['struct_title'],
                "struct_acronym": struc['struct_acronym'],
                "structure_id": struc['struct_id']
            }
        )
