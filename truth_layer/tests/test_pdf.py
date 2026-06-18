from services.pdf_extractor import (
    PDFExtractor
)


def test_pdf_extraction():

    data = PDFExtractor.extract(
        "sample.pdf"
    )

    assert (
        "full_text"
        in data
    )