
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load OpenAI key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
base_dir = Path(__file__).resolve().parent
script_dir = base_dir / "generated_scripts_for_tester_evaluation"
review_dir = base_dir / "generated_tester_agent_outputs"
output_dir = base_dir / "llm_judge_evaluations"
output_dir.mkdir(parents=True, exist_ok=True)

# Define the models used in Step 2's tester agent
model_versions = ["gpt-4", "gpt-35-turbo"]

# Evaluation loop
for script_file in script_dir.glob("*.py"):
    with open(script_file, "r") as f:
        script_content = f.read()

    for model_version in model_versions:
        model_tag = model_version.replace(".", "")  # e.g., gpt-3.5-turbo -> gpt-35-turbo
        review_file = review_dir / (script_file.stem + f"_{model_tag}_test_report.txt")
        
        if not review_file.exists():
            print(f"Review missing for {model_version}: {review_file.name}")
            continue

        with open(review_file, "r") as f:
            tester_output = f.read()

        # LLM prompt
        prompt = f"""
You are an expert judge evaluating the performance of an AI tester agent.

Below is a Python script and the review generated by the tester agent.

Evaluate the review on these three criteria:
1. Accuracy (Did the tester correctly identify real issues?)
2. Helpfulness (Are the suggestions meaningful and useful?)
3. Coverage (Did the review miss major issues?)

Give scores from 1 to 5 (5 = best) for each.

Respond in this JSON format:
{{
  "score": [average],
  "accuracy": [1-5],
  "helpfulness": [1-5],
  "coverage": [1-5],
  "comments": "[brief reasoning]"
}}

--- BEGIN SCRIPT ---
{script_content}
--- END SCRIPT ---

--- BEGIN TESTER REVIEW ({model_version}) ---
{tester_output}
--- END TESTER REVIEW ---
"""

        # Call LLM judge
        response = client.chat.completions.create(
            model="gpt-4",  # Judge model is GPT-4 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        evaluation = response.choices[0].message.content

        # Save with model-specific judge score
        output_file = output_dir / (script_file.stem + f"_{model_tag}_judge_score.json")
        with open(output_file, "w") as f:
            f.write(evaluation)

        print(f"✅ Judge scored ({model_version}): {output_file.name}")
