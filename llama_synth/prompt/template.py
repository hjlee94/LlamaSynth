from typing import Callable, List, NewType

TemplateGetter = NewType("TemplateGetter", Callable[[str], str])

def get_classification_template(label_names:List[str]) -> TemplateGetter:
    def template(inp:str) -> str:
        labels = ", ".join(label_names)
        prompt = f"Classify the Input into {labels}\n"
        prompt += f"Input:{inp}\n"
        prompt += f"Label:"
        return prompt

    return template
