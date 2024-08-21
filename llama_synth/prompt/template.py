from typing import Callable, List

def classification_template(label_name:List[str]) -> Callable[[str], str]:
    def template(inp:str) -> Callable[[str], str]:
        prompt = f"Classify the text into {", ".join(label_name)}\n"
        prompt += f"Input:{inp}\n"
        prompt += f"Label:"
        return prompt

    return template
