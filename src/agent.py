# src/agent.py
from src.embedder import load_embedder
from src.retriever import load_faiss_index, load_csv_to_documents, build_faiss_index, load_pdfs_to_documents, load_online_documents
from src.llm_core import load_model_pipeline
from src.rag_pipeline import build_rag_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

class RAGAgent:
    def __init__(
        self,
        index_path: str = "src/knowledgebase/index/",
        model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        embed_model: str = "all-MiniLM-L6-v2",
        whether_online: bool = False
    ):
        self.embedder = load_embedder(embed_model)

        self.docs = self.load_data()
        
        self.build_index()
        
        self.retriever = load_faiss_index(self.embedder, index_path)

        self.llm = load_model_pipeline(model_name)

        self.qa_chain = build_rag_chain(self.llm, self.retriever)
        
        self.whether_online = whether_online

    def answer_with_knowledge(self, query: str) -> str:
        if self.whether_online:
            from src.search_engine import fetch_docs_from_search
            docs_list = fetch_docs_from_search(query)
            
            self.retriever.add_documents(docs_list)

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
        online_docs = load_online_documents()
        docs.extend(csv_docs)
        docs.extend(pdf_docs)
        docs.extend(online_docs)
        print(f"Loaded {len(docs)} documents from online sources.")
        # docs = self.chunk_documents(docs)
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
        build_faiss_index(self.docs, self.embedder)
        

# PYTHONPATH=. python RAG/src/agent.py
if __name__ == "__main__":
    agent = RAGAgent(whether_online=True)
    query = "What is CVA"
    response = agent.answer_with_knowledge(query)
    print(response)