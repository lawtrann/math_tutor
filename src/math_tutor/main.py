#!/usr/bin/env python
import os
from typing import Any, Dict, Optional

from crewai.flow import Flow, listen, or_, router, start
from langtrace_python_sdk import langtrace
from pydantic import BaseModel

from math_tutor.constant import ALGEBRA, GEOMETRY, STATISTICS
from math_tutor.crews.algebra.algebra_tutor import AlgebraTutor
from math_tutor.crews.geometry.geometry_tutor import GeometryTutor
from math_tutor.crews.math_classifier.math_classifier import MathClassifier
from math_tutor.crews.math_classifier.model.question import Question
from math_tutor.crews.statistics.statistics_tutor import StatisticsTutor


class MathTutorState(BaseModel):
    inputs: Optional[Dict[str, Any]] = None
    question: Optional[Question] = None


class MathTutorFlow(Flow[MathTutorState]):
    langtrace.init(api_key=os.environ.get('LANGTRACE_API_KEY'))
    language = "Japanese"

    algebra = str(ALGEBRA).lower()
    geometry = str(GEOMETRY).lower()
    statistics = str(STATISTICS).lower()

    total_cost = 0.0

    @start()
    def handle_input(self):
        question_content = input("Input your question: ")
        inputs = {
            'language': self.language,
            'question_content': question_content,
            'algebra': self.algebra,
            'geometry': self.geometry,
            'statistics': self.statistics,
        }
        self.state.inputs = inputs

    @listen(handle_input)
    def determine_math_domain(self):
        result = (
            MathClassifier()
            .crew()
            .kickoff(inputs=self.state.inputs)
        )

        self.state.question = Question(**result.to_dict())

        # gemini-2.0-flash
        costs = (0.1 * result.token_usage.prompt_tokens + 0.4 * result.token_usage.completion_tokens) / 1_000_000
        print("Costs of determine_math_domain: ", costs)
        self.total_cost += costs

    @router(determine_math_domain)
    def handle_math_domain(self):
        match self.state.question.domain.lower():
            case self.algebra:
                return "algebra"
            case self.geometry:
                return "geometry"
            case self.statistics:
                return "statistics"
            case _:
                return "unknown"

    @listen("algebra")
    def solve_algebra(self):
        question = self.state.question

        tutor_inputs = {
            "language": self.language,
            "domain": question.domain,
            "question": question.question,
        }

        result = AlgebraTutor().crew().kickoff(inputs=tutor_inputs)

        # gemini-1.5-flash-8b
        costs = (0.0375 * result.token_usage.prompt_tokens + 0.15 * result.token_usage.completion_tokens) / 1_000_000
        print("Costs of solve_algebra: ", costs)
        self.total_cost += costs

    @listen("geometry")
    def solve_geometry(self):
        question = self.state.question

        tutor_inputs = {
            "language": self.language,
            "domain": question.domain,
            "question": question.question,
            "image_path": question.image_path,
        }

        result = GeometryTutor().crew().kickoff(inputs=tutor_inputs)

        costs = (0.1 * result.token_usage.prompt_tokens + 0.4 * result.token_usage.completion_tokens) / 1_000_000
        print("Costs of solve_algebra: ", costs)
        self.total_cost += costs

    @listen("statistics")
    def solve_statistics(self):
        question = self.state.question

        tutor_inputs = {
            "language": self.language,
            "domain": question.domain,
            "question": question.question,
        }

        result = StatisticsTutor().crew().kickoff(inputs=tutor_inputs)

        costs = (0.1 * result.token_usage.prompt_tokens + 0.4 * result.token_usage.completion_tokens) / 1_000_000
        print("Costs of solve_algebra: ", costs)
        self.total_cost += costs

    @listen("unknown")
    def solve_unknown(self):
        print("Unknown domain")

    @listen(or_(solve_algebra, solve_geometry, solve_statistics, solve_unknown))
    def end(self):
        print("Total costs: ", self.total_cost)


def kickoff():
    MathTutor_flow = MathTutorFlow()
    MathTutor_flow.kickoff()


def plot():
    MathTutor_flow = MathTutorFlow()
    MathTutor_flow.plot()


if __name__ == "__main__":
    kickoff()
