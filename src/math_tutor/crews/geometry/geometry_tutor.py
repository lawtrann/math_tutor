from crewai import Agent, Crew, Process, Task
from crewai.project import agent, crew, CrewBase, task

from math_tutor.tools.vision_tool import VisionTool


@CrewBase
class GeometryTutor():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def math_tutor(self) -> Agent:
        return Agent(
            config=self.agents_config['math_tutor'],
        )

    @task
    def solve_question(self) -> Task:
        return Task(
            config=self.tasks_config['solve_question'],
            tools=[VisionTool()],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
        )
