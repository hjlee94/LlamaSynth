from llama_cpp import Llama
from .prompt.base import Prompt
from . import errors

import yaml

class LlamaSpeaker:
    def __init__(self, name:str, model_path:str, prompt:Prompt=None, max_tokens:int=256, **kwargs) -> None:
        self.name = name
        
        self._llm = Llama(
            model_path=model_path,
            verbose=False,
            n_ctx=2048
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
        )

        self._llm_param = {}
        self.set_generation_mode()
        self._llm_param.update(kwargs)

        self.prompt = prompt

        self._max_tokens = max_tokens

    @classmethod
    def from_card(cls, path) -> "Prompt":
        with open(path, 'r') as fd:
            data = yaml.load(fd, Loader=yaml.CLoader)

        prompt = Prompt(
            system_prompt=data.get("system_prompt", ""),
            template=None
        )
        
        return cls(name=data["name"], model_path=data["model_path"], prompt=prompt)

    def set_generation_mode(self):
        self._llm_param['temperature'] = 0.8
        self._llm_param['top_p'] = 0.95
        self._llm_param['frequency_penalty'] = 0.0

    def set_classification_mode(self) -> None:
        self._llm_param['top_p'] = 1.0
        self._llm_param['frequency_penalty'] = 0
        self._llm_param['presence_penalty'] = 0

    def set_prompt(self, prompt:Prompt):
        self.prompt = prompt

    def __call__(self, question:str) -> str:
        if not self.prompt:
            raise errors.AgentException("You must set the prompt obejct for LlamaSpeaker")
        
        text = self.prompt.get_prompt(question=question, history_k=4)
        
        output = self._llm(text, max_tokens=self._max_tokens, 
                           **self._llm_param)

        choices = output['choices']
        answer = choices[0]['text'].strip()

        self.prompt.history.append_chat(question=question, answer=answer)

        return answer
