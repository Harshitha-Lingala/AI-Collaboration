# src/research_agent/research_agent.py
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import openai
from crewai import Crew, Task, Agent
from crewai_tools import SerperDevTool
from langchain_community.llms import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ResearchAgent:
    def __init__(self):
        parameters = {"temperature": 0.7, "max_tokens": 500}
        self.llm = OpenAI(model_name="gpt-4", **parameters)
        self.function_calling_llm = OpenAI(model_name="gpt-4", **parameters)
        self.search = SerperDevTool()

        self.agent = Agent(
            llm=self.llm,
            function_calling_llm=self.function_calling_llm,
            role="Senior Data Science Researcher",
            goal="Analyze ML problems and recommend the best approaches.",
            backstory=(
                "You are a top data science researcher skilled at understanding real-world ML problems "
                "and identifying ideal solutions, including preprocessing and algorithm selection."
            ),
            allow_delegation=False,
            tools=[self.search],
            verbose=True,
        )

    def generate_task(self, problem_statement):
        search_results = self.search.run(search_query=f"{problem_statement} machine learning algorithms", n_results=3)
        search_summary = "\n".join([f"{r['title']} - {r['snippet']}" for r in search_results.get("organic", [])])

        return Task(
            description=(
                f"Given the problem statement '{problem_statement}', "
                "suggest the best algorithms, preprocessing steps, and model types to solve the problem.\n\n"
                f"Search Summary: {search_summary}"
            ),
            expected_output="Bullet point list of recommended techniques with justification.",
            output_file="generated_outputs/researcher_agent_output.txt",
            agent=self.agent,
        )

    def analyze(self, problem_statement):
        task = self.generate_task(problem_statement)
        crew = Crew(agents=[self.agent], tasks=[task], verbose=True)
        return crew.kickoff()
    
