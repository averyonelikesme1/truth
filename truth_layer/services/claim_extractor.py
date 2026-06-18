from __future__ import annotations

from typing import Dict
from typing import List

from services.gemini_client import GeminiClient

from prompts.claim_prompt import (
    CLAIM_EXTRACTION_PROMPT
)

from utils.logger import logger


class ClaimExtractor:

    def __init__(self):

        self.gemini = GeminiClient()

    def extract_claims(
        self,
        document_text: str
    ) -> List[Dict]:

        try:

            prompt = CLAIM_EXTRACTION_PROMPT.format(
                document_text=document_text[:80000]
            )

            result = self.gemini.generate_json(
                prompt
            )

            claims = result.get(
                "claims",
                []
            )

            logger.info(
                f"Claims extracted: {len(claims)}"
            )

            return claims

        except Exception as e:

            logger.exception(
                f"Claim extraction failed: {str(e)}"
            )

            return []