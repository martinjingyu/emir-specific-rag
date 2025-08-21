from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter

def load_text_documents(folder_path="data/docs"):
    loader = TextLoader(folder_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)