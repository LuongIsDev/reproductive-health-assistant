import os
import sys
# Insert current directory at the beginning of sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from agents.agent_coordinator import CoordinatorAgent
    print("SUCCESS: Imported CoordinatorAgent from local agents")
    print("Local agents path:", os.path.dirname(CoordinatorAgent.__module__.replace('.', os.sep)))
except Exception as e:
    print("STILL FAILED:", e)
    import traceback
    traceback.print_exc()
