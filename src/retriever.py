from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader


import pandas as pd
import os

def build_faiss_index(docs, embedder, save_path="src/knowledgebase/index/"):
    vectorstore = FAISS.from_documents(docs, embedder)
    vectorstore.save_local(save_path)

def load_faiss_index(embedder, path="src/knowledgebase/index/"):
    
    return FAISS.load_local(path, embedder, allow_dangerous_deserialization=True).as_retriever()

def load_csv_to_documents():
    docs = []
    folder_path = "src/knowledgebase/csv"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():

                content = str(row.get("Answers", ""))
                question = str(row.get("Questions", filename))  
                docs.append(Document(page_content=question + ": "+ content, metadata={"title": question}))
    
    return docs

def load_pdfs_to_documents(folder_path="src/knowledgebase/pdf"):
    docs = []
    if not os.path.isdir(folder_path):
        return docs

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".pdf"):
            continue
        file_path = os.path.join(folder_path, filename)

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        for i, p in enumerate(pages, start=1):
            docs.append(
                Document(
                    page_content=p.page_content,
                    metadata={
                        **p.metadata,
                        "source": filename,
                        "page": i,
                        "type": "pdf",
                    },
                )
            )
    return docs