import os
import sys

# Get the project root (parent of scratch)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"First path: {sys.path[0]}")

try:
    from agents.agent_coordinator import CoordinatorAgent
    print("SUCCESS: Imported CoordinatorAgent from local agents")
    import agents
    print("Agents location:", agents.__file__)
except Exception as e:
    print("STILL FAILED:", e)
    import traceback
    traceback.print_exc()
