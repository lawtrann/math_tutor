from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, CrewBase, task

from math_tutor.crews.math_classifier.model.question import Question
from math_tutor.tools.vision_tool import VisionTool


@CrewBase
class MathClassifier():
    """MathClassifier crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def math_teacher(self) -> Agent:
        return Agent(
            config=self.agents_config['math_teacher'],
        )

    @task
    def determine_domain(self) -> Task:
        return Task(
            config=self.tasks_config['determine_domain'],
            tools=[VisionTool()],
            output_pydantic=Question,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MathClassifier crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )
