# book_rag_chain.py
import os
import chromadb
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def get_rag_chain():
    prompt = ChatPromptTemplate.from_template('''\
        以下の文章だけを踏まえて回答してください。

        文脈: """
        {context}
        """

        質問: {question}                                      
    ''')

    model = ChatOpenAI(name='gpt-4.1-nano-2025-04-14')

    collection_name = os.getenv("CHROMA_COLLECTION_NAME")
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(),
    )
    
    chain = (
        {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain