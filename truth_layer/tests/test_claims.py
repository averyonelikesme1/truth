from services.claim_extractor import (
    ClaimExtractor
)


def test_claim_extraction():

    extractor = ClaimExtractor()

    claims = (
        extractor.extract_claims(
            """
            India population
            crossed 1.4 billion.
            """
        )
    )

    assert isinstance(
        claims,
        list
    )