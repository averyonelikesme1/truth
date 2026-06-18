from pathlib import Path


def validate_pdf(
    file_name: str
) -> bool:

    return (
        Path(file_name)
        .suffix
        .lower()
        == ".pdf"
    )


def chunk_text(
    text: str,
    size: int = 25000
):

    chunks = []

    for i in range(
        0,
        len(text),
        size
    ):
        chunks.append(
            text[i:i+size]
        )

    return chunks