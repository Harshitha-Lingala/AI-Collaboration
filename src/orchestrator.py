import os
import json
import sys
from pathlib import Path

# Ensure the parent directory is included in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.developer_agent.developer_agent import DeveloperAgent
from src.tester_agent.tester_agent import AITesterAgent

class CollaborationOrchestrator:
    def __init__(self):
        self.developer = DeveloperAgent()
        self.tester = AITesterAgent()
        self.state_path = Path("collaboration_state.json")

    def run(self, requirements, max_iterations=2): #change iterations here
        feedback = None

        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*40}\nIteration {iteration}/{max_iterations}\n{'='*40}")

            # Generate/revise code
            code = self.developer.generate_code(requirements, feedback)
            print(f"\nGenerated Code:\n{'-'*30}\n{code}\n{'-'*30}")

            # Save state
            self._save_state(code, feedback)

            # Test code
            test_result = self.tester.test_script(code)
            print(f"\nTest Results:\n{'-'*30}\n{test_result}\n{'-'*30}")

            # If code passes, save and exit
            if "No critical issues found" in test_result:
                print("\n✅ All tests passed!")
                self._save_final_code(code)
                return code

            feedback = test_result  # Update feedback for next iteration

        print("\n❌ Maximum iterations reached")
        return code

    def _save_state(self, code, feedback):
        """Save current collaboration state"""
        self.state_path.write_text(json.dumps({"code": code, "feedback": feedback}, indent=2))

    def _save_final_code(self, code):
        """Save final validated code"""
        output_path = Path("final_code.py")
        output_path.write_text(code)
        print(f"Final code saved to {output_path.absolute()}")
