from langchain_ollama import OllamaLLM
from state import AgentState
from utils import extract_code
import subprocess
import os


# Initialize Ollama
llm = OllamaLLM(model="llama3.2:3b")

def programmer_node(state: AgentState):
    print(f"--- ATTEMPT {state['iterations'] + 1} ---")
    
    # Construct the prompt based on whether an error exists
    if state['error']:
        feedback_prompt = f"""
        Your previous code failed with the following error:
        {state['error']}
        
        Please analyze the error and rewrite the Python script to fix it.
        Original Task: {state['task']}
        Return ONLY the code inside ```python ``` blocks.
        """
    else:
        feedback_prompt = f"""
        Write a Python script to perform the following task: {state['task']}
        Return ONLY the code inside ```python ``` blocks.
        """

    response = llm.invoke(feedback_prompt)
    cleaned_code = extract_code(response)
    
    return {
        "code": cleaned_code,
        "iterations": state['iterations'] + 1
    }

def executor_node(state: AgentState):
    file_path = "temp_script.py"
    
    # 1. Write the code to a temporary file
    with open(file_path, "w") as f:
        f.write(state['code'])
    
    # 2. Run the script using subprocess
    try:
        # We use 'python' because uv's venv is activated
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10 # Prevent infinite loops in the script itself
        )
        
        if result.returncode == 0:
            print("✅ Execution Successful!")
            return {"error": None}
        else:
            print("❌ Execution Failed!")
            # Capture the stderr (the Python Traceback)
            return {"error": result.stderr}
            
    except Exception as e:
        return {"error": str(e)}