from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import requests

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')


def run(params: ActionParams) -> None:
    """Index documents and allow Q&A"""
    folder = None
    for ent in params['entities']:
        if ent['entity'] == 'path':
            folder = ent['resolution']['value']
            break
    if folder is None:
        return leon.answer({'key': 'error'})

    try:
        reader = SimpleDirectoryReader(folder)
        docs = reader.load_data()
        client = chromadb.PersistentClient(path=os.path.join(folder, '.chroma'))
        vector_store = ChromaVectorStore(chroma_client=client, collection_name='docs')
        index = VectorStoreIndex.from_documents(docs, vector_store=vector_store)
        index.storage_context.persist()
        leon.answer({'key': 'done'})
    except Exception:
        leon.answer({'key': 'error'})
