import os
import json
import sys
from pathlib import Path

# Ensure the parent directory is included in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.developer_agent.developer_agent import DeveloperAgent
from src.tester_agent.tester_agent import AITesterAgent
from src.research_agent.research_agent import ResearchAgent

class CollaborationOrchestrator:
    def __init__(self):
        self.researcher = ResearchAgent()
        self.developer = DeveloperAgent()
        self.tester = AITesterAgent()
        self.state_path = Path("collaboration_state.json")


    def run(self, user_problem, max_iterations=2):
    # STEP 1: Use Research Agent to generate insights
        print("\n Running Research Agent...")
        research_output = self.researcher.analyze(user_problem)
        print(f"\n Research Agent Output:\n{research_output}")

        # STEP 2: Combine research insights with original requirements
        full_requirements = (
            f"Problem: {user_problem}\n\n"
            f"Recommended Approach (from Research Agent):\n{research_output}"
        )
        print('-------------------------------------------------')
        print(full_requirements)
        print('-------------------------------------------------')

        # best_model = self.researcher.extract_best_model(research_output)
        # print(f"\n Best Model Selected: {best_model['model_name']}")
        
        # # Pass only the best model's details to the developer
        # full_requirements = (
        #     f"Problem: {user_problem}\n\n"
        #     f"Best Model for this problem: {best_model['model_name']}\n"
        #     f"Preprocessing steps: {best_model['preprocessing_steps']}\n"
        #     f"Implementation guidelines: {best_model['implementation_guidelines']}\n"
        #     "Now, develop the model based on these guidelines."
        # )
        # #developer_prompt

        # print('-------------------------------------------------')
        # print(full_requirements)
        # print('-------------------------------------------------')

        # STEP 3: Pass to Developer + Tester loop
        feedback = None
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*40}\nIteration {iteration}/{max_iterations}\n{'='*40}")
            code = self.developer.generate_code(full_requirements, feedback)
            print(f"\nGenerated Code:\n{'-'*30}\n{code}\n{'-'*30}")

            self._save_state(code, feedback)

            test_result = self.tester.test_script(code)
            print(f"\nTest Results:\n{'-'*30}\n{test_result}\n{'-'*30}")

            if "No critical issues found" in test_result:
                print("\n All tests passed!")
                self._save_final_code(code)
                return code

            feedback = test_result

        print("\n Maximum iterations reached")
        return code


    def _save_state(self, code, feedback):
        """Save current collaboration state"""
        self.state_path.write_text(json.dumps({"code": code, "feedback": feedback}, indent=2))

    def _save_final_code(self, code):
        """Save final validated code"""
        output_path = Path("generated_outputs/final_code_generated.py")
        output_path.write_text(code)
        print(f"Final code saved to {output_path.absolute()}")


