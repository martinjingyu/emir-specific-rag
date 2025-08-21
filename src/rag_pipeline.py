from langchain.chains import RetrievalQA
from src.llm_core import HuggingFaceChatLLM
from src.search_engine import fetch_texts_from_search
def build_rag_chain(llm: HuggingFaceChatLLM, retriever):
    
    def compose_prompt_fn(query):

        docs = retriever.invoke(query)
        
        online_doc = fetch_texts_from_search(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        context = context + "\n\n" + online_doc
        context = llm.self_refine(query, context)
        # print(context)
        
        prompt = llm.compose_prompt(context=context, query=query)
        return prompt

    def qa_fn(query: str):
        prompt = compose_prompt_fn(query)
        return llm._call(prompt)

    return qa_fn