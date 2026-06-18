from __future__ import annotations

import json

import google.generativeai as genai

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

from utils.logger import logger


class GeminiClient:

    def __init__(self):

        genai.configure(
            api_key=GEMINI_API_KEY
        )

        self.model = genai.GenerativeModel(
            GEMINI_MODEL
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=10
        )
    )
    def generate_json(
        self,
        prompt: str
    ) -> dict:

        try:

            response = self.model.generate_content(
                prompt
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = (
                    text
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            return json.loads(text)

        except Exception as e:

            logger.exception(
                f"Gemini API error: {str(e)}"
            )

            raise
        