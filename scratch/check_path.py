import sys
import os
print("Current directory:", os.getcwd())
print("sys.path:")
for p in sys.path:
    print(f"  {p}")

try:
    import agents
    print("Found agents at:", agents.__file__)
except ImportError:
    print("agents package not found")
except Exception as e:
    print("Error importing agents:", e)
