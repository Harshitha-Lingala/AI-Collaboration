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
            f"Script Name: {script_name}\n"
            "Script:\n" + script_content
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content
