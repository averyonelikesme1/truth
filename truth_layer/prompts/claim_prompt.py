CLAIM_EXTRACTION_PROMPT = """
You are an expert fact-checking analyst.

Your task is to identify all claims that require verification.

Extract:

1. Statistics
2. Percentages
3. Financial figures
4. Scientific statements
5. Technical facts
6. Dates
7. Historical facts
8. Quantitative claims
9. Government or policy claims
10. Medical claims

Rules:

- Ignore opinions.
- Ignore marketing language.
- Ignore recommendations.
- Extract only verifiable factual statements.

Return JSON only.

Expected format:

{
  "claims":[
    {
      "claim":"...",
      "type":"statistic",
      "page_reference":"page number if known"
    }
  ]
}

Document:

{document_text}
"""