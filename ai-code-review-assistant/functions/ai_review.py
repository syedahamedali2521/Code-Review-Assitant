import os
from openai import OpenAI

def get_ai_review(code, language):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Perform a professional code review.

    Language: {language}
    Code:
    {code}

    Return issues, improvements, best practices, and optimization suggestions.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        return response.choices[0].message["content"]

    except Exception as e:
        return f"Error during AI review: {e}"

