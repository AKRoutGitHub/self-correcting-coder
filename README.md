# 🤖 The Self-Correcting Python Coder

An autonomous coding agent that writes, executes, and self-repairs Python scripts. Built using **LangGraph**, **Ollama (Llama 3.2:3b)**, and **UV Package Manager**.

Unlike standard LLM prompts, this agent uses a **State Machine (Directed Acyclic Graph)** to catch execution errors and feed them back into the model for automatic debugging until the code runs successfully.

---

## 🚀 Key Features

* **Agentic Self-Correction:** Implements a feedback loop where `stderr` tracebacks are used as prompts for the model.
* **Local-First Execution:** Powered by **Ollama**, ensuring your code logic stays on your local machine.
* **Graph-Based Logic:** Uses **LangGraph** to manage state and conditional routing between the "Programmer" and "Executor" nodes.
* **Fast Environment Management:** Optimized with the **UV** package manager for near-instant dependency handling.

---

## 🛠️ Setup & Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AKRoutGitHub/self-correcting-coder.git
    cd self-correcting-coder
    ```

2.  **Initialize Environment (Using UV):**
    ```bash
    # Create venv and install dependencies
    uv venv
    source .venv/Scripts/activate  # Git Bash / Windows
    uv add langgraph langchain-ollama
    ```

3.  **Local LLM Setup:**
    Ensure [Ollama](https://ollama.com/) is running and you have the model:
    ```bash
    ollama pull llama3.2:3b
    ```

---

## 📖 How to Use

1.  **Define your Task:**
    Open `main.py` and modify the `task` in the `initial_state` dictionary:
    ```python
    "task": "Write a script that scrapes a title from a website, but intentionally use a wrong library name to test the self-correction."
    ```

2.  **Run the Agent:**
    ```bash
    python main.py
    ```

3.  **Watch the Logs:**
    The agent will stream its progress. You will see it:
    * **📍 Node: programmer** (Writes the initial code)
    * **📍 Node: executor** (Runs code and catches errors)
    * **⚠️ Error Detected** (The agent identifies the crash)
    * **🔁 Loop** (The programmer fixes the code based on the traceback)

---

## ⚙️ Technical Workflow

1.  **The Programmer Node:** Generates Python code using a system prompt that mandates output in clean Markdown blocks.
2.  **The Executor Node:** Saves code to `temp_script.py` and executes it via a Python `subprocess`.
3.  **Conditional Routing:** - If `Exit Code == 0` → Graph ends.
    - If `Exit Code != 0` → Error is captured and sent back to the Programmer.
4.  **State Management:** Tracks `iterations` to prevent infinite loops (default max: 5).

---

## 🌟 Coming Soon (Roadmap)

- [ ] **Multi-File Projects:** Expansion to allow the agent to edit multiple files in a directory.
- [ ] **Pip-Install Node:** Ability for the agent to automatically `uv add` missing libraries it detects in `ModuleNotFoundError`.
- [ ] **Reviewer Node:** Adding a third "Critic" node to check code quality/security before execution.
- [ ] **Web Interface:** A basic UI to visualize the graph transitions in real-time.

---

## 👤 Author
**Asish**
* **GitHub:** [@AKRoutGitHub](https://github.com/AKRoutGitHub)
* **Project Goal:** Mastering Agentic AI workflows and maintaining a consistent GitHub contribution streak.
