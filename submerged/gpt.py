import base64
import logging
import os
from typing import Optional

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def generate_description_with_gpt(image_bytes: bytes) -> Optional[str]:
    """
    Sends the image to OpenAI GPT-4 Vision and returns the generated description.

    Args:
        image_bytes: The raw bytes of the image file.

    Returns:
        The generated description as a string, or None if an error occurs.
    """
    try:
        # Encode image to base64
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_mime_type = (
            "image/jpeg"  # Assuming JPEG, adjust if needed or detect dynamically
        )

        logger.info("Sending image to OpenAI for analysis...")

        # Call OpenAI API (ensure you use a model supporting vision, e.g., gpt-4-vision-preview or gpt-4o)
        response = await openai_client.chat.completions.create(
            model="gpt-4o",  # Or "gpt-4-vision-preview" - use the latest available vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Describe the fish or marine life visible in this image. Identify the species if possible and provide a short, engaging description or interesting fact about it. Write in Russian",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{image_mime_type};base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,  # Adjust max tokens as needed for description length
        )

        # Extract the description text
        if (
            response.choices
            and response.choices[0].message
            and response.choices[0].message.content
        ):
            description = response.choices[0].message.content.strip()
            logger.info("Successfully received description from OpenAI.")
            return description
        else:
            logger.warning("OpenAI response did not contain the expected content.")
            return None

    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}", exc_info=True)
        return None
