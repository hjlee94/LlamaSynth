from typing import List, Dict

class History:
    def __init__(self) -> None:
        self._history = []

    def append_chat(self, question, answer):
        self._history.append(
            dict(q=question, a=answer)
        )

    def get_chat_history(self, last=0):
        if last > 0:
            return self._history[-last:]
        
        return self._history

class PromptGenerator:
    def __init__(self, system_prompt:str) -> None:
        self._system_prompt = f"<|start_header_id|>system<|end_header_id|>"
        self._system_prompt+= f"{system_prompt}<|eot_id|>"

    @staticmethod
    def get_user_prompt(question:str):
        prompt = f"<|start_header_id|>user<|end_header_id|>"
        prompt += f"{question}<|eot_id|>"
        return prompt

    @staticmethod
    def get_assistant_prompt(answer:str="") -> str:
        prompt = f"<|start_header_id|>assistant<|end_header_id|>"
        if answer:
            prompt += f"{answer}<|eot_id|>"

        return prompt

    def get_prompt(self, question:str, chat_history:History=None, history_k=2) -> str:
        prompt = f"{self._system_prompt}"

        if chat_history:
            for h in chat_history.get_chat_history(last=history_k):
                hq = h['q']; ha = h['a']

                prompt += self.get_user_prompt(question=hq)
                prompt += self.get_assistant_prompt(answer=ha)

        prompt += self.get_user_prompt(question=question)
        prompt += self.get_assistant_prompt()

        return prompt


