from datetime import datetime
import json
from pathlib import Path
import sys

from config import schema
from utils import file_utils

DATA_ROUTE = "data/transcripts"
CURRENT_DATE = datetime.now().strftime("%d-%m-%Y")
OUTPUT_PATH = f"results/Evaluation[{CURRENT_DATE}].json"

if __name__ == "__main__":

    transcripts = file_utils.extract_transcripts(DATA_ROUTE)
    
    total_transcripts = len(transcripts)
    evaluation_results: dict[str, schema.TranscriptEvaluation] = {}

    for index, (key, content) in enumerate(transcripts.items(), start=1):
        sys.stdout.write(
            f"\rProcessing [{index}/{total_transcripts}]: {key}".ljust(60)
        )
        sys.stdout.flush()

    print(f"\nFinished evaluating {total_transcripts} transcripts.")

    output_file = Path(OUTPUT_PATH)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        serializable_data = {
            k: v.model_dump() if hasattr(v, "model_dump") else v
            for k, v in evaluation_results.items()
        }
        json.dump(serializable_data, f, indent=4, ensure_ascii=False)

    print(f"Results saved to: {OUTPUT_PATH}")