from typing import List, Callable

from llama_cpp import Llama
from .prompt.manager import History, PromptManager
from .prompt import template

import yaml

class LlamaSpeaker:

    @classmethod
    def from_card(cls, path):
        with open(path, 'r') as fd:
            data = yaml.load(fd, Loader=yaml.CLoader)
        
        return cls(**data)

    def __init__(self, model_path, name, system_prompt="", max_tokens=256, **kwargs) -> None:
        self.name = name
        
        self._llm = Llama(
            model_path=model_path,
            verbose=False,
            n_ctx=2048
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
        )
        self._prompt = PromptManager(
            system_prompt=system_prompt
        )

        self._llm_param = {}
        self._llm_param['temperature'] = 0.8
        self._llm_param['top_p'] = 0.95
        self._llm_param['frequency_penalty'] = 0.0
        self._llm_param.update(kwargs)

        self._history = History()

        self._max_tokens = max_tokens

    def set_classification_mode(self, label_name:List[str]):
        self._llm_param['top_p'] = 1.0
        self._llm_param['frequency_penalty'] = 0
        self._llm_param['presence_penalty'] = 0

        self._prompt.set_template(
            template.classification_template(label_name)
        )

    def clear_history(self):
        self._history.clear()

    def generate(self, q):
        text = self._prompt.get_prompt(question=q, chat_history=self._history, history_k=4)
        output = self._llm(text, max_tokens=self._max_tokens, 
                           **self._llm_param)

        choices = output['choices']
        answer = choices[0]['text'].strip()

        self._history.append_chat(question=q, answer=answer)

        return answer
