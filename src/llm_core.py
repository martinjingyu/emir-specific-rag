from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain_community.llms import HuggingFacePipeline
from langchain_core.language_models import LLM
import torch
class HuggingFaceChatLLM:
    
    def __init__(self, model_name):
        
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            model_max_length=2048
        )
        
    def _call(self, input_ids) -> str:

        output_ids = self.model.generate(input_ids)
        generated_ids = output_ids[0][input_ids.shape[-1]:]

        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response

    def compose_prompt(self, context: str, query: str) -> str:
        messages = [
            {"role": "system", "content": f"You are a helpful assistant in financial area."},
            {"role": "user", "content":f"Here are some information you might be able to use:\n{context}. \nHere is the question:\n{query}"}
        ]
        return self.tokenizer.apply_chat_template([messages], tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
    
    def generate(self, query: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant in financial area."},
            {"role": "user", "content": query}]
        input_ids = self.tokenizer.apply_chat_template([messages], tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
        
        response = self._call(input_ids)
        return response
    def self_refine(self, query: str, context: str) -> str:
        retriever_system_prompt = """
        You are the retriever component of a Retrieval-Augmented Generation (RAG) system.
        Given a user question and a context, your task is to determine whether the context contains information that is relevant to answering the question.
            •	If relevant information exists, extract or point to the relevant parts.
            •	If no relevant information is present, respond with: “No relevant information found.”
        Be precise and avoid assuming facts not supported by the context."""
        quiry_for_retrieve = [{"role": "system", "content": retriever_system_prompt},
                              {"role": "user", "content": f"Here is the question: {query}\nHere is the context: {context}"}]
        
        quiry = [
            {"role": "system", "content": "You are a helpful assistant in financial area."},
            {"role": "user", "content": query}]
        
        messages = [quiry_for_retrieve, quiry]
        input_ids = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")

        output_ids = self.model.generate(input_ids)
        
        output_list = []
        for i in range(len(output_ids)):
            
            generated_ids = output_ids[i][input_ids[i].shape[-1]:]

            response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
            output_list.append(response)
        
        if "no relevant information found" in output_list[0].lower():
            return output_list[1]
        else:
            return output_list[0]
    

def load_model_pipeline(model_name="meta-llama/Llama-2-7b-chat-hf"):

    hf_pipeline = HuggingFaceChatLLM(model_name = model_name)
    
    return hf_pipeline