import re

def parse_output(output: str) -> str:
    """
    Cleans up LLM output by:
    - Removing leading/trailing whitespace
    - Removing hallucinated "Answer:" or "Response:"
    - Stripping markdown artifacts
    """

    # Remove hallucinated prefixes like "Answer:", "Response:"
    output = re.sub(r"^(Answer:|Response:)\s*", "", output.strip(), flags=re.IGNORECASE)

    # Remove markdown headers or symbols
    output = re.sub(r"^#+\s*", "", output, flags=re.MULTILINE)

    # Remove excessive newlines or double spaces
    output = re.sub(r"\n{3,}", "\n\n", output)
    output = re.sub(r"\s{2,}", " ", output)

    return output.strip()
