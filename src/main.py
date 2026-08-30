from datetime import datetime
import json
from pathlib import Path
import sys
from dotenv import load_dotenv
import time


from config import schema
from utils import file_utils
from evaluator import evaluate_transcript

DATA_ROUTE = "data/transcripts"
OUTPUT_PATH = "../results/grades.json"
BATCH_SIZE = 5

if __name__ == "__main__":

    transcripts = file_utils.extract_transcripts(DATA_ROUTE)
    
    total_transcripts = len(transcripts)
    evaluation_results: dict[str, schema.TranscriptEvaluation] = {}

    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "grades.json"

    sorted_transcripts = sorted(transcripts.items())

    for index, (key, content) in enumerate(sorted_transcripts, start=1):

        eval_result = evaluate_transcript(transcript_id=key, content=content)

        if isinstance(eval_result, dict) and "error" in eval_result:
            evaluation_results[key] = {
                "id": key,
                "error": eval_result["error"]
            }
        else:
            evaluation_results[key] = {
                "id": key,
                "total": eval_result.total_score,
                "criteria": eval_result.model_dump()
            }

        if index % BATCH_SIZE == 0 or index == total_transcripts:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(evaluation_results, f, indent=4, ensure_ascii=False)

        # TODO: REMOVE, this is only a countermeasure to my free tier model rate limits.
        if index < total_transcripts:
            time.sleep(4.5)

    print(f"Results saved to: {OUTPUT_PATH}")