from typing import Optional

from pydantic import BaseModel, Field


class Question(BaseModel):
    domain: str = Field(..., description="The domain of the question.")
    question: str = Field(..., description="The question to be answered.")
    answer_options: Optional[list] = Field(None, description="The answer options to the question.")
    image_path: Optional[str] = Field(None, description="the path to the image of the question.")
