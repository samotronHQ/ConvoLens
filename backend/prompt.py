def build_prompt(chat_text):
    return f"""
You are an expert relationship analyst.

Analyze the conversation and return STRICT JSON only.

Chat:
{chat_text}

Return this exact JSON format:

{{
  "participants": ["A", "B"],
  "initiation_ratio": 0.5,
  "response_effort": 0.7,
  "emotional_tone": {{
    "A": {{
      "tone": "short tone label",
      "explanation": "natural human explanation"
    }},
    "B": {{
      "tone": "short tone label",
      "explanation": "natural human explanation"
    }}
  }},
  "imbalance": {{
    "status": "None/Low/Medium/High",
    "dominant_participant": "participant name or None detected",
    "least_engaged": "participant name or None detected",
    "explanation": "short explanation"
  }},
  "red_flags": [
    {{
      "label": "behavioral label",
      "severity": "Low/Medium/High",
      "explanation": "why this is concerning",
      "evidence": "exact text from chat"
    }}
  ],
  "green_flags": []
    {{
      "label": "positive behavior label",
      "explanation": "why this is positive",
      "evidence": "exact text from chat"
    }}
  ],
  "communication_pattern": {{
    "pattern": "short descriptive label",
    "explanation": "overall interaction pattern"
  }},
  "summary": "short summary"
}}

Rules:
- Identify ALL participants from the chat.
- participants MUST include every speaker, like ["A", "B", "C"].
- emotional_tone MUST include every participant.
- Use decimal numbers only, like 0.5, not 1/2.
- Do NOT use None or null. Use "None detected".
- red_flags and green_flags MUST be arrays.
- Return ONLY valid JSON.
- Do NOT wrap output in markdown.
- least_engaged must be the participant with minimal contribution.
- green_flags must represent genuinely positive behaviors only.
- Use natural, non-robotic explanations.
- Do NOT include comments like /* ... */ inside JSON.
- If there are no green flags, return "green_flags": [].
- If there are no red flags, return "red_flags": [].
"""