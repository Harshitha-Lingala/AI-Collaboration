
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AITesterAgent:
    def __init__(self, model="gpt-4"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def test_script(self, script_content, script_name="Generated Code"):
        """Analyzes script for errors and suggests improvements."""
        prompt = (
            "You are an AI tester. Review the script for:\n"
            "- Syntax errors\n- Logical issues\n- Runtime problems\n"
            "- Improperly initialized components\n- Incorrect method calls\n"
            "- Missing dependencies\n- Unused modules\n\n"
            "-or any other errors that you notice"
            f"Script Name: {script_name}\n"
            "Script:\n" + script_content
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        output = response.choices[0].message.content

        # Ensure the output directory exists
        output_dir = "generated_outputs"
        os.makedirs(output_dir, exist_ok=True)

        # Write the output to a file
        output_path = os.path.join(output_dir, "tester_agent_output.txt")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(output)

        return output
