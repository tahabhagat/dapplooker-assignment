from google import genai
from google.genai import types
from loguru import logger
from models.llm_models import TokenInsightInput, TokenInsights

client = genai.Client()

prompt = """
You are a Quant Analyst. Considering the provided input data for a given token, generate a sentiment, as well as reasoning of 2-3 sentences for the given sentiment.
Consider the following input data for a given token:
```token_data
{input}
```
Generate the sentiment (Bullish, Neutral, or Bearish) and reasoning for the token.
"""

config = types.GenerateContentConfig(
    temperature=2,
    response_json_schema=TokenInsights.model_json_schema(),
    response_mime_type="application/json",
)


def generate_insights(input: TokenInsightInput) -> TokenInsights:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt.format(input=input), config=config
    )
    logger.info(f"Generated insights for token {input.token.id}: {response.text}")

    # Explicitly convert the parsed response to TokenInsights
    if response.parsed is not None:
        return TokenInsights.model_validate(response.parsed)
    else:
        # Handle the case where parsing failed
        raise ValueError("Failed to parse response from LLM model")
