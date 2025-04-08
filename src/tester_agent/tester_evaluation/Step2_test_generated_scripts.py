
import os
import sys
from pathlib import Path

# Set up paths
current_file = Path(__file__).resolve()
src_path = current_file.parents[3] / "src"
sys.path.insert(0, str(src_path))

from tester_agent.tester_agent import AITesterAgent

# Paths
base_dir = current_file.parent
input_dir = base_dir / "generated_scripts_for_tester_evaluation"
output_dir = base_dir / "generated_tester_agent_outputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Models to compare
models = ["gpt-4", "gpt-3.5-turbo"]

# Loop through models and scripts
for model_name in models:
    tester = AITesterAgent(model=model_name)
    model_tag = model_name.replace(".", "")  

    for file in input_dir.glob("*.py"):
        with open(file, "r") as f:
            script_content = f.read()

        print(f"Testing {file.name} with {model_name}...")

        test_output = tester.test_script(script_content, script_name=file.name)

        # Save with model-specific filename
        output_file = output_dir / (file.stem + f"_{model_tag}_test_report.txt")
        with open(output_file, "w") as f:
            f.write(test_output)

        print(f" Saved: {output_file.name}")
