from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from prompt import build_prompt
import os
import json
import re

load_dotenv("../.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    chat: str

@app.post("/analyze")
def analyze_chat(data: ChatInput):
    prompt = build_prompt(data.chat)

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Return ONLY valid JSON."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=1200
)

    ai_output = response.choices[0].message.content.strip()

    
    ai_output = ai_output.replace(": None", ': "None detected"')
    ai_output = ai_output.replace(": null", ': "None detected"')

    def fix_fraction(match):
        num = float(match.group(1))
        den = float(match.group(2))
        return str(round(num / den, 2))

    
    ai_output = re.sub(r'/\*.*?\*/', '', ai_output, flags=re.DOTALL)
    ai_output = re.sub(r'(\d+)\s*/\s*(\d+)', fix_fraction, ai_output)

    try:
        parsed_output = json.loads(ai_output)
        return {"analysis": parsed_output}

    except Exception:
        print("AI OUTPUT ERROR:", ai_output)

        return {
            "analysis": {
                "summary": "Your stand is too strong. Try a shorter chat snippet.",
                "emotional_tone": {},
                "response_effort": 0,
                "red_flags": [],
                "green_flags": [],
                "imbalance": {},
                "initiation_ratio": 0
            }
        }