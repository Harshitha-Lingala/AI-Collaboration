import os
from tester_agent import AITesterAgent

def main():
    script_filename = "housing_prices_prediction.py"  # File to test
    script_path = os.path.join(os.path.dirname(__file__), script_filename)

    # Read the content of the .py file
    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    # Create tester agent and test the script
    tester = AITesterAgent(model="gpt-4")
    output = tester.test_script(script_content, script_name=script_filename)

    # Optionally print the output
    print("\n=== Tester Agent Output ===\n")
    print(output)

if __name__ == "__main__":
    main()
