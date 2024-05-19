from weaviate import WeaviateClient
from weaviate.classes.config import Property, DataType, Configure
from weaviate.util import generate_uuid5
import distyll
from distyll.utils import chunk_text
import distyll.config
from distyll.config import CHUNK_COLLECTION

def prep_db(client: WeaviateClient) -> None:
    """
    Prepare the database for use
    :param client: Weaviate client
    :return: None
    """
    if client.collections.exists(CHUNK_COLLECTION):
        pass
    else:
        client.collections.create(
            CHUNK_COLLECTION,
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="url", data_type=DataType.TEXT, skip_vectorization=True),
                Property(name="chunk", data_type=DataType.TEXT),
                Property(name="chunk_no", data_type=DataType.INT),
            ],
            vectorizer_config=[
                Configure.NamedVectors.text2vec_ollama(
                    name="default",
                    model="snowflake-arctic-embed:33m",
                    api_endpoint="http://host.docker.internal:11434",
                    vector_index_config=Configure.VectorIndex.hnsw(
                        quantizer=Configure.VectorIndex.Quantizer.bq()
                    ),
                ),
            ],
            generative_config=Configure.Generative.ollama(
                model="mistral:7b",
                api_endpoint="http://host.docker.internal:11434",
            ),
        )


def add_yt_to_db(client: WeaviateClient, yt_url) -> int:
    """
    Add a YouTube video to the database
    :param client: Weaviate client
    :param yt_url: YouTube URL
    :return: Number of chunks added
    """
    prep_db(client)
    transcript_data = distyll.transcripts.from_youtube(yt_url)
    chunks_collection = client.collections.get(CHUNK_COLLECTION)
    chunk_no = 0
    with chunks_collection.batch.fixed_size() as batch:
        for t in transcript_data["transcripts"]:
            for _, transcript in enumerate(transcript_data["transcripts"]):
                for chunk in chunk_text(transcript):
                    batch.add_object(
                        properties={
                            "title": transcript_data["title"],
                            "url": transcript_data["yt_url"],
                            "chunk": chunk,
                            "chunk_no": chunk_no,
                        },
                        uuid=generate_uuid5(chunk),
                    )
                    chunk_no += 1
    print(f"Added {chunk_no} chunks to the database")
    return chunk_no


def add_text_to_db(client: WeaviateClient, text: str, title: str = "", src_url: str = "") -> int:
    """
    Add a YouTube video to the database
    :param client: Weaviate client
    :param text: Un-chunked text
    :return: Number of chunks added
    """
    prep_db(client)
    chunks_collection = client.collections.get(CHUNK_COLLECTION)
    chunk_no = 0
    with chunks_collection.batch.fixed_size() as batch:
        for chunk in chunk_text(text):
            batch.add_object(
                properties={
                    "title": title,
                    "url": src_url,
                    "chunk": chunk,
                    "chunk_no": chunk_no,
                },
                uuid=generate_uuid5(chunk),
            )
            chunk_no += 1
    print(f"Added {chunk_no} chunks to the database")
    return chunk_no


def add_arxiv_to_db(client: WeaviateClient, arxiv_url: str) -> int:
    """
    Add an arXiv paper to the database
    :param client: Weaviate client
    :param arxiv_url: arXiv URL
    :return: Number of chunks added
    """
    prep_db(client)
    paper_data = distyll.text.from_arxiv_paper(arxiv_url)
    chunks_collection = client.collections.get(CHUNK_COLLECTION)
    chunk_no = 0
    with chunks_collection.batch.fixed_size() as batch:
        for chunk in chunk_text(paper_data["text"]):
            batch.add_object(
                properties={
                    "title": paper_data["title"],
                    "url": paper_data["url"],
                    "chunk": chunk,
                    "chunk_no": chunk_no,
                },
                uuid=generate_uuid5(chunk),
            )
            chunk_no += 1
    print(f"Added {chunk_no} chunks to the database")
    return chunk_no


def add_pdf_to_db(client: WeaviateClient, pdf_url: str, title: str = "") -> int:
    """
    Add an arXiv paper to the database
    :param client: Weaviate client
    :param pdf_url: PDF URL
    :return: Number of chunks added
    """
    prep_db(client)
    text = distyll.text.from_pdf(pdf_url)
    chunks_collection = client.collections.get(CHUNK_COLLECTION)
    chunk_no = 0
    with chunks_collection.batch.fixed_size() as batch:
        for chunk in chunk_text(text):
            batch.add_object(
                properties={
                    "title": title,
                    "url": pdf_url,
                    "chunk": chunk,
                    "chunk_no": chunk_no,
                },
                uuid=generate_uuid5(chunk),
            )
            chunk_no += 1
    print(f"Added {chunk_no} chunks to the database")
    return chunk_no
