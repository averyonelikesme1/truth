from services.verifier import (
    FactVerifier
)


def test_fact_verification():

    verifier = FactVerifier()

    result = verifier.verify_claim(
        "Earth is flat"
    )

    assert (
        "verdict"
        in result
    )
    