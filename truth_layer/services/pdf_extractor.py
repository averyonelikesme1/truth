from __future__ import annotations

import fitz
from pathlib import Path
from typing import Dict, List

from utils.logger import logger


class PDFExtractor:
    """
    Extract text from PDF while preserving page references.
    """

    @staticmethod
    def extract(pdf_path: str | Path) -> Dict:
        try:
            document = fitz.open(pdf_path)

            pages: List[Dict] = []
            full_text = []

            for page_number in range(len(document)):
                page = document[page_number]

                text = page.get_text("text")

                pages.append(
                    {
                        "page": page_number + 1,
                        "text": text
                    }
                )

                full_text.append(
                    f"[PAGE {page_number + 1}]\n{text}"
                )

            logger.info(
                "PDF extraction completed successfully."
            )

            return {
                "page_count": len(document),
                "pages": pages,
                "full_text": "\n".join(full_text)
            }

        except Exception as e:
            logger.exception(
                f"PDF extraction failed: {str(e)}"
            )

            raise RuntimeError(
                f"Unable to process PDF: {str(e)}"
            )