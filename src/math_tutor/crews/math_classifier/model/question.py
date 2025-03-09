from typing import Optional

from pydantic import BaseModel, Field


class Question(BaseModel):
    domain: str = Field(..., description="the mathematics domain of the question.")
    question: str = Field(..., description="the full question content without image path.")
    image_path: Optional[str] = Field(None, description="the path to the image of the question for the geometry domain only.")
