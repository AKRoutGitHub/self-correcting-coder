import re

def extract_code(text: str) -> str:
    # Regex to find content between ```python and ```
    pattern = r"```python\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    # Fallback if the LLM didn't use markdown blocks
    return text.strip()