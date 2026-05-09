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
  "green_flags": [
    {{
      "label": "positive behavior label",
      "explanation": "why this is positive. If this is generous, say it is a slightly generous interpretation.",
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
- initiation_ratio must always be between 0 and 1.
- response_effort must always be between 0 and 1.
- Use decimal numbers only, like 0.5, not 1/2.
- Do NOT use None or null. Use "None detected".
- Do NOT include comments like /* ... */ inside JSON.
- If there are no green flags, return "green_flags": [].
- If there are no red flags, return "red_flags": [].
- Be slightly generous when identifying green_flags, especially in neutral or ambiguous interactions.
- Green flags can include mild positives like effort to respond, engagement, or maintaining conversation.
- Do NOT invent strong positives if none exist — only mild or tentative positives.
- Keep every explanation under 20 words.
- Keep summary under 25 words.
- red_flags and green_flags MUST be arrays.
- Return ONLY valid JSON.
- Do NOT wrap output in markdown.
- least_engaged must be the participant with minimal contribution.
- green_flags must represent genuinely positive or mildly positive behaviors only.
- Use natural, non-robotic explanations.
"""