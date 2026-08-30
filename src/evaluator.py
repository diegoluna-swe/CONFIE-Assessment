import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai
from google.genai import types
import yaml

from config import schema

yaml_path = Path(__file__).parent / "config/config.yaml"
with open(yaml_path, "r", encoding="utf-8") as f:
    config_dict = yaml.safe_load(f)


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = config_dict["SYSTEM_PROMPT"].replace(
    "{CRITERIA}", config_dict["CRITERIA"]
)

def evaluate_transcript(transcript_id: str, content: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries):
        try:
            print(f"Evaluating {transcript_id}...", end="\r", flush=True)            
            
            response = client.models.generate_content(
                model=config_dict["MODEL_ID"],  
                contents=f"Transcript ID: {transcript_id}\nContent:\n{content}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=float(config_dict.get("TEMPERATURE", 1.0)),
                    response_mime_type="application/json",
                    response_schema=schema.TranscriptEvaluation,
                ),
            )

            eval_result: schema.TranscriptEvaluation = response.parsed
            return eval_result

        except Exception as e:
            print(f"\nAttempt {attempt + 1} failed to evaluate {transcript_id}: {e}")
            if attempt == max_retries - 1:
                print(f"Max retries reached for {transcript_id}. Returning error.")
                return {"error": str(e)}