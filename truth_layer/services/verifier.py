from __future__ import annotations

from typing import Dict
from typing import List

from services.gemini_client import GeminiClient
from services.wikipedia_client import WikipediaClient
from services.search_client import SearchClient

from prompts.verification_prompt import (
    FACT_VERIFICATION_PROMPT
)

from utils.logger import logger


class FactVerifier:

    def __init__(self):

        self.search = SearchClient()

        self.wiki = WikipediaClient()

        self.gemini = GeminiClient()

    def verify_claim(
        self,
        claim: str
    ) -> Dict:

        try:

            search_results = (
                self.search.search_claim(claim)
            )

            if not search_results:

                return {
                    "claim": claim,
                    "verdict": "INACCURATE",
                    "confidence": 0,
                    "correct_fact": "No evidence found",
                    "explanation": "Search returned no evidence.",
                    "sources": []
                }

            evidence_text = "\n\n".join(
                [
                    (
                        f"Title: {item['title']}\n"
                        f"Content: {item['content']}\n"
                        f"URL: {item['url']}"
                    )
                    for item in search_results
                ]
            )

            prompt = (
                FACT_VERIFICATION_PROMPT
                .format(
                    claim=claim,
                    evidence=evidence_text
                )
            )

            result = (
                self.gemini.generate_json(
                    prompt
                )
            )

            result["claim"] = claim

            result["sources"] = [
                item["url"]
                for item in search_results
            ]

            logger.info(
                f"Verification complete: {claim}"
            )

            return result

        except Exception as e:

            logger.exception(
                f"Verification failed: {str(e)}"
            )

            return {
                "claim": claim,
                "verdict": "INACCURATE",
                "confidence": 0,
                "correct_fact": "Error occurred",
                "explanation": str(e),
                "sources": []
            }

    def verify_batch(
        self,
        claims: List[Dict]
    ) -> List[Dict]:

        verified_claims = []

        for claim_obj in claims:

            claim_text = claim_obj.get(
                "claim",
                ""
            )

            if not claim_text:
                continue

            result = self.verify_claim(
                claim_text
            )

            result["type"] = claim_obj.get(
                "type",
                "unknown"
            )

            result["page_reference"] = (
                claim_obj.get(
                    "page_reference",
                    "N/A"
                )
            )

            verified_claims.append(
                result
            )

        return verified_claims