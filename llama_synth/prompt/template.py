from typing import Callable, List

type TemplateGetter = Callable[[str], str]

def get_classification_template(label_names:List[str]) -> TemplateGetter:
    def template(inp:str) -> str:
        prompt = f"Classify the Input into {", ".join(label_names)}\n"
        prompt += f"Input:{inp}\n"
        prompt += f"Label:"
        return prompt

    return template
