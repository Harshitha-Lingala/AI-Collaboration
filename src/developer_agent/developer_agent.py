import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DeveloperAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate_code(self, requirements, feedback=None):
        """Generates/refines code based on requirements and previous feedback."""
        prompt = (
            "You are an AI Developer agent specialized in writing production-ready code.\n"
            "Follow industry best practices including comments, modular functions, and error handling.\n\n"
            f"Requirements: {requirements}\n"
        )
        if feedback:
            prompt += f"Previous feedback: {feedback}\n"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content
