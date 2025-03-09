import base64
from typing import Any, Type

from crewai.tools import BaseTool
from litellm import completion
from pydantic import BaseModel, Field


class VisionToolSchema(BaseModel):
    """Input schema for VisionGoogleTool."""

    image_path: str = Field(..., description="Path to the image file.")
    additional_context: str = Field("", description="The additional context that you need to ask for more visual to solve the question such as geometry.")


class VisionTool(BaseTool):
    name: str = "Vision Tool"
    description: str = "This tool uses an Gemini's API to extract content from an image file."

    args_schema: Type[BaseModel] = VisionToolSchema

    def _run(self, **kwargs: Any) -> str:
        image_path = kwargs.get("image_path")
        if image_path is None:
            return "There is no image path provided."

        if image_path.startswith("http"):
            image_data = image_path
        else:
            with open(image_path, 'rb') as f:
                img_bytes = f.read()

            img_b64 = base64.b64encode(img_bytes).decode('utf-8')
            image_data = f"data:image/png;base64,{img_b64}"

        try:
            resp = completion(
                model="gemini/gemini-2.0-flash",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "To meticulously extract full content from a given picture without solving problem. Format to Markdown, no '```'. "
                                        f"{kwargs.get('additional_context')}",
                            },
                            {
                                "type": "image_url",
                                "image_url": image_data,
                            }
                        ]
                    }
                ]
            )

            return resp.choices[0].message.content
        except Exception as e:
            return str(e)
