from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from .utils import trim_parse_form
import torch

class LLM:
    def fill_form(self, user_message: str) -> Dict[str, str]:
        ...

class Llama(LLM):
    pipe: Any = None

    def __init__(self, model: str, adapter: str = None):
        if not self.pipe:
            tokenizer = AutoTokenizer.from_pretrained(model)
            model = AutoModelForCausalLM.from_pretrained(
                model,
                torch_dtype=torch.bfloat16,
                attn_implementation='flash_attention_2',
                device_map='auto'
            )
            tokenizer.pad_token_id = tokenizer.eos_token_id
            if adapter:
                model.load_adapter(adapter)
            self.pipe = pipeline(
                'text-generation',
                model=model,
                tokenizer=tokenizer,
                torch_dtype=torch.bfloat16,
                device_map='auto'
            )

    def fill_form(self, user_message: str) -> Dict[str, str]:
        messages = [
            {'role': 'user', 'content': user_message}
        ]
        outputs = self.pipe(messages, max_new_tokens=256)
        message = outputs[0]['generated_text'][-1]
        return trim_parse_form(message['content'])

class OpenAI(LLM):
    def __init__(self, base_url: str, api_key: str, model: str):
        self.model = ChatOpenAI(base_url=base_url, api_key=api_key, model=model)

    def fill_form(self, user_message: str) -> Dict[str, str]:
        parser = RunnableLambda(lambda x: trim_parse_form(x.content))
        prompt = ChatPromptTemplate.from_messages([
            ('user', user_message)
        ])
        chain = prompt | self.model | parser
        return chain.invoke({})
