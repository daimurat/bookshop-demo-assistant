from gc import collect
import os
import json
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def ingest_data():
    print("Ingesting data...")

    # OpenAI埋め込みモデルのインスタンスを作成
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    # Chromaコレクションへ保存
    collection_name = os.getenv("CHROMA_COLLECTION_NAME")
    persist_dir = "./chroma_db"

    # Chromaへの接続確認: persist_directoryがなければ作成
    if not os.path.exists(persist_dir):
        os.makedirs(persist_dir)
    # Chromaのインスタンス作成で接続確認
    try:
        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory=persist_dir,
        )
    except Exception as e:
        print(f"Chromaへの接続に失敗しました: {e}")
        return
    
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

    # Chromaにデータを追加
    try:
        vectorstore.add_documents(documents)
        print(f"Added {len(documents)} books to Chroma collection '{collection_name}'.")
    except Exception as e:
        print(f"Chromaへのデータ追加に失敗しました: {e}")
        raise