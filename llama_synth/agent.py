from llama_cpp import Llama
from .utils import History, PromptManager

import yaml

class LlamaSpeaker:

    @classmethod
    def from_card(cls, path):
        with open(path, 'r') as fd:
            data = yaml.load(fd, Loader=yaml.CLoader)
        
        return cls(**data)

    def __init__(self, model_path, name, system_prompt="", max_tokens=256) -> None:
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

        self._history = History()

        self._max_tokens = max_tokens

    def clear_history(self):
        self._history.clear()

    def generate(self, q):
        text = self._prompt.get_prompt(question=q, chat_history=self._history, history_k=4)
        output = self._llm(text, max_tokens=self._max_tokens, temperature=0.9, top_p=0.95, frequency_penalty=0.1)

        choices = output['choices']

        if len(choices) > 1:
            #! it is required to compare scores?
            print(f"multiple!!!", choices)

        answer = choices[0]['text'].strip()

        self._history.append_chat(question=q, answer=answer)

        return answer
