import base64
from typing import Any, Type, Dict

from crewai.tools import BaseTool
from litellm import completion
from pydantic import BaseModel, Field

# Global cache dictionary to store image data
_IMAGE_CACHE: Dict[str, str] = {}

class VisionToolSchema(BaseModel):
    """Input schema for VisionGoogleTool."""

    image_path: str = Field(..., description="Path to the image file.")
    additional_context: str = Field("", description="The additional context that you need to ask for more visual to solve the question such as geometry.")


class VisionTool(BaseTool):
    name: str = "Vision Tool"
    description: str = "This tool uses an Gemini's API to extract content from an image file."

    args_schema: Type[BaseModel] = VisionToolSchema

    @staticmethod
    def _get_image_data(image_path: str) -> str:
        """Get image data from cache or process it if not cached."""
        # Return URL directly if it's a web image
        if image_path.startswith("http"):
            return image_path
            
        # Check if image data is in cache
        if image_path in _IMAGE_CACHE:
            print("Hit cache!!!")
            return _IMAGE_CACHE[image_path]
        
        # Process and cache image data if not found
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        image_data = f"data:image/png;base64,{img_b64}"
        
        # Store in cache
        _IMAGE_CACHE[image_path] = image_data
        return image_data

    def _run(self, **kwargs: Any) -> str:
        image_path = kwargs.get("image_path")
        if image_path is None:
            return "There is no image path provided."

        # Get image data from cache or process it
        image_data = self._get_image_data(image_path)

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
