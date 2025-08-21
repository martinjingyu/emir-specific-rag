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
        

    @property
    def _llm_type(self) -> str:
        return "custom-huggingface-chat"


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


def load_model_pipeline(model_name="meta-llama/Llama-2-7b-chat-hf"):

    hf_pipeline = HuggingFaceChatLLM(model_name = model_name)
    
    return hf_pipeline