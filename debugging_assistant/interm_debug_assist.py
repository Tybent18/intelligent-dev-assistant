import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ai_suggest_fix(code_text, error_msg):
    """Generate AI-based debugging suggestions."""
    
    if not client.api_key:
        return "AI suggestions unavailable (no API key set)."

    prompt = f"""
You are a senior Python developer.

Code:
{code_text}

Error:
{error_msg}

Explain the issue clearly and provide a corrected version of the code.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI suggestion failed: {e}"