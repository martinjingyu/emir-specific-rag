from langchain.chains import RetrievalQA
from src.llm_core import HuggingFaceChatLLM
from src.search_engine import fetch_docs_from_search
def build_rag_chain(llm: HuggingFaceChatLLM, retriever):
    
    def compose_prompt_fn(query):

        docs = retriever.invoke(query)
        

        context = "\n\n".join(doc.page_content for doc in docs)
        # context = llm.self_refine(query, context)

        prompt = llm.compose_prompt(context=context, query=query)
        return prompt

    def qa_fn(query: str):
        prompt = compose_prompt_fn(query)
        return llm._call(prompt)

    return qa_fn