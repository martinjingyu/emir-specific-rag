# src/agent.py
from src.embedder import load_embedder
from src.retriever import load_faiss_index, load_csv_to_documents, build_faiss_index, load_pdfs_to_documents
from src.llm_core import load_model_pipeline
from src.rag_pipeline import build_rag_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGAgent:
    def __init__(
        self,
        index_path: str = "src/knowledgebase/index/",
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        embed_model: str = "all-MiniLM-L6-v2"
    ):
        self.embedder = load_embedder(embed_model)

        self.docs = self.load_data()
        
        self.build_index()
        
        self.retriever = load_faiss_index(self.embedder, index_path)

        self.llm = load_model_pipeline(model_name)

        self.qa_chain = build_rag_chain(self.llm, self.retriever)

    def answer_with_knowledge(self, query: str) -> str:
        result = self.qa_chain(query)
        print(f"Query: {query}\nResult: {result}")
        return result
    
    def direct_answer(self, query: str) -> str:
        """
        Directly answer the query without using RAG.
        This is a placeholder for future implementation.
        """
        # For now, we just return a placeholder response
        response = self.llm.generate(query)
        return response

    def load_data(self):
        docs = []
        csv_docs = load_csv_to_documents()
        pdf_docs = load_pdfs_to_documents()
        docs.extend(csv_docs)
        docs.extend(pdf_docs)
        
        docs = self.chunk_documents(docs)
        return docs
    
    
    def chunk_documents(self, docs, chunk_size=1000, chunk_overlap=150):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        return splitter.split_documents(docs)
    def build_index(self):
        build_faiss_index(self.docs, self.embedder, save_path="src/knowledge/index/")