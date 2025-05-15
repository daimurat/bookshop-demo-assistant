from gc import collect
import os
import json
from langchain_chroma.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    # catalogue.jsonのロード
    with open("./data/catalogue.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Documentリストを作成
    documents = []
    for book in data["books"]:
        content = f"{book['title']} ({book['author']})\n{book['description']}\n{book['toc']}"
        metadata = {
            "id": book["id"],
            "category": book["category"],
            "pages": book["pages"]
        }
        documents.append(Document(page_content=content, metadata=metadata))

    # OpenAI埋め込みモデルのインスタンスを作成
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    # Chromaコレクションへ保存
    collection_name = os.getenv("CHROMA_COLLECTION_NAME")
    vectorstore = Chroma.from_documents(
        documents,
        embedding=embedding,
        persist_directory="./chroma_db",
        collection_name=collection_name,
    )

    print(f"Loaded {len(documents)} books into Chroma collection '{collection_name}'.")