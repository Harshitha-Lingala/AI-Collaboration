from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import re
import random

# Load environment variables from .env file
load_dotenv()

#  Initialize OpenAI client using the key from the .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-3.5-turbo"

#  Dynamically get the path relative to this script's location
base_dir = Path(__file__).resolve().parent
output_dir = base_dir / "generated_scripts_for_tester_evaluation"
output_dir.mkdir(parents=True, exist_ok=True)

# Extract just the Python code from markdown-like LLM responses
def extract_python_code(text: str) -> str:
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()

# programmatic bug injection 
def inject_bug(code: str) -> str:
    bugs = [
        lambda c: re.sub(r"import pandas as pd", "", c),
        lambda c: re.sub(r"\.fit\(", "# .fit(", c),
        lambda c: c.replace("train_test_split", "split_data_function"),
        lambda c: c.replace("LinearRegression", "LinearRegressor"),
    ]
    return random.choice(bugs)(code)

# Prompts for diverse buggy script generation
prompts = [
    "Build a machine learning model to predict house prices using the Boston Housing Dataset. Include evaluation using MSE and R².",
    "Create a script to scrape product titles from an e-commerce site using BeautifulSoup and requests.",
    "Build a sentiment analysis classifier using logistic regression on a text dataset like IMDB.",
    "Implement a basic image classifier using CNNs in PyTorch. Use CIFAR-10 or MNIST.",
    "Write a script that fetches weather data from an API and stores it in a CSV file with proper error handling.",
]

# Generate scripts for each prompt
for i, prompt in enumerate(prompts, start=1):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI Developer agent specialized in writing complete, production-ready code based on user requirements."},
            {"role": "user", "content": f"{prompt} Introduce 1-2 small bugs or poor practices in the code for testing purposes."}
        ],
        temperature=0.7
    )

    raw_output = response.choices[0].message.content
    generated_code = extract_python_code(raw_output)

    # apply additional bug injection 
    # generated_code = inject_bug(generated_code)

    # Generate filename based on task and timestamp
    title = prompt[:40].lower().replace(" ", "_").replace(",", "").replace(".", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"task_{i}_{title}_{timestamp}.py"

    # Save the script
    full_path = output_dir / filename
    with open(full_path, "w") as f:
        f.write(generated_code)

    print(f" Saved: {filename}")
