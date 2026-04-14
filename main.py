from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import programmer_node, executor_node

# 1. Initialize the Graph
workflow = StateGraph(AgentState)

# 2. Add our nodes
workflow.add_node("programmer", programmer_node)
workflow.add_node("executor", executor_node)

# 3. Define the Flow
workflow.set_entry_point("programmer")

# From Programmer, we always go to Executor
workflow.add_edge("programmer", "executor")

# 4. Define Conditional Logic (The Loop)
def should_continue(state: AgentState):
    # If there's no error, we are done!
    if state["error"] is None:
        return END
    # If we've tried too many times (e.g., 5), stop to avoid wasting resources
    if state["iterations"] >= 5:
        print("--- MAX ITERATIONS REACHED ---")
        return END
    # Otherwise, go back to the programmer to fix the error
    return "programmer"

workflow.add_conditional_edges(
    "executor",
    should_continue,
    {
        "programmer": "programmer",
        END: END
    }
)

# 5. Compile the Graph
app = workflow.compile()

# 6. Run it!
if __name__ == "__main__":
    initial_state = {
        "task": "Create a list of 5 numbers, then try to print the 10th element to trigger an error, then fix it to only print available elements.",
        "code": "",
        "error": None,
        "iterations": 0
    }
    # app.invoke(initial_state)

    print("🚀 Starting Agentic Loop...\n" + "="*30)

    # .stream() returns an iterator of snapshots as the graph moves through nodes
    for snapshot in app.stream(initial_state):
        for node_name, state_update in snapshot.items():
            print(f"\n📍 CURRENT NODE: {node_name}")
            print("-" * 20)
            
            # Show if an error was captured
            if "error" in state_update and state_update["error"]:
                print(f"⚠️ Error Detected: {state_update['error'].strip().splitlines()[-1]}")
            
            # Show the iteration count
            if "iterations" in state_update:
                print(f"🔢 Iteration: {state_update['iterations']}")
            
            # Optional: Show a snippet of the generated code
            if "code" in state_update and state_update["code"]:
                first_line = state_update["code"].strip().splitlines()[0]
                print(f"💻 Code Preview: {first_line}...")
    print("\n" + "="*30 + "\n✅ Process Finished.")