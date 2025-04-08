import os
from dotenv import load_dotenv
import re

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Debug check
# print("OPENAI_API_KEY from env:", os.getenv("OPENAI_API_KEY"))

from src.orchestrator import CollaborationOrchestrator

if __name__ == "__main__":
    system = CollaborationOrchestrator()

    requirements = (
     "Build a Machine Learning model to suit IRIS Dataset."   
    )

    output = system.run(requirements)

    # Extract only the code part from the response
    match = re.search(r"```python\n(.*?)```", output, re.DOTALL)
    final_code = match.group(1) if match else output  # fallback to raw output if no match

    #  Save the final code to a Python file
    with open("generated_outputs/final_code_generated.py", "w") as f:
        f.write(final_code)

    print("\n Final code saved to final_code.py")
    
