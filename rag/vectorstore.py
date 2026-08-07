"""
Vectorstore Chroma (Bloc 2 — RAG)
Pattern officiel LangChain + langchain-chroma.
"""
from functools import lru_cache

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from rag.documents import DOCS
from config.settings import CHROMA_PATH, COLLECTION_NAME, OPENAI_EMBEDDING_MODEL


@lru_cache(maxsize=2)
def get_vectorstore(persist: bool = True) -> Chroma:
    """
    Crée ou charge le vectorstore Chroma.
    Lazy : appelé seulement quand on en a besoin.
    """
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    if persist:
        store = Chroma(
            embedding_function=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name=COLLECTION_NAME,
        )
        if not store.get(limit=1)["ids"]:
            store.add_documents(DOCS)
        return store
    return Chroma.from_documents(
        documents=DOCS,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
    )


def get_retriever(k: int = 3):
    """Retriever officiel LangChain."""
    vs = get_vectorstore()
    return vs.as_retriever(search_kwargs={"k": k})