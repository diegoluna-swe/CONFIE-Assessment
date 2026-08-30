import csv
import json
from pathlib import Path


def run_evaluation():
    # Routing
    base_dir = Path(__file__).resolve().parent.parent
    latest_json = base_dir / "results" / "grades.json"
    labels_csv = base_dir / "labels.csv"

    if not latest_json.exists():
        print("No evaluation JSON found. Run main.py first.")
        return

    if not labels_csv.exists():
        print(f"Error: Target labels file not found at {labels_csv}")
        return

    # Message
    print(f"Analyzing evaluation file: {latest_json.name}")

    ai_data = json.loads(latest_json.read_text(encoding="utf-8"))

    human_labels = {}

    with open(labels_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            t_id = row["call_id"]

            # Target subset C001 - C015
            if t_id in [f"C{str(i).zfill(3)}" for i in range(1, 16)]:
                human_labels[t_id] = {
                    "c1_greeting": int(row["c1_greeting"]),
                    "c2_needs_discovery": int(row["c2_discovery"]),
                    "c3_compliance": int(row["c3_compliance"]),
                    "c4_resolution": int(row["c4_resolution"]),
                    "c5_professionalism": int(row["c5_professionalism"]),
                }

    criteria_keys = [
        "c1_greeting",
        "c2_needs_discovery",
        "c3_compliance",
        "c4_resolution",
        "c5_professionalism",
    ]

    exact_matches = 0
    within_5_matches = 0
    total_evals = 0
    absolute_errors = []

    # Store disagreements so they can be reviewed later
    disagreements = []

    print("\n--- Evaluation Report (C001 - C015) ---")

    for i in range(1, 16):
        t_id = f"C{i:03d}"

        if t_id not in ai_data:
            print(f"Warning: {t_id} missing from AI results JSON.")
            continue

        if t_id not in human_labels:
            print(f"Warning: {t_id} missing from human labels CSV.")
            continue

        ai_criteria = ai_data[t_id].get("criteria", {})
        human_criteria = human_labels[t_id]

        call_disagreements = []

        for crit in criteria_keys:
            if crit not in ai_criteria:
                print(
                    f"⚠️ Key Error: '{crit}' not found in AI data "
                    f"for {t_id}. Defaulting to 0."
                )

            ai_val = int(ai_criteria.get(crit, 0))
            human_val = int(human_criteria.get(crit, 0))

            total_evals += 1

            error = abs(ai_val - human_val)
            absolute_errors.append(error)

            if ai_val == human_val:
                exact_matches += 1

            if error <= 5:
                within_5_matches += 1

            if ai_val != human_val:
                call_disagreements.append({
                    "criterion": crit,
                    "ai": ai_val,
                    "human": human_val,
                    "error": error,
                })

        if call_disagreements:
            disagreements.append({
                "call_id": t_id,
                "disagreements": call_disagreements,
            })

    if total_evals > 0:
        accuracy = (exact_matches / total_evals) * 100
        within_5_accuracy = (within_5_matches / total_evals) * 100
        mae = sum(absolute_errors) / total_evals

        print(f"\nTotal Evaluated Points: {total_evals}")
        print(f"Calls Evaluated:        {total_evals // 5}")
        print(f"Exact Match Accuracy:   {accuracy:.2f}%")
        print(f"Within 5 Points:        {within_5_accuracy:.2f}%")
        print(f"Mean Absolute Error:    {mae:.2f}")

        # Print individual disagreements
        print("\n--- Disagreements ---")

        if not disagreements:
            print("No disagreements found.")
        else:
            for call in disagreements:
                print(f"\n{call['call_id']}")

                for disagreement in call["disagreements"]:
                    print(
                        f"  {disagreement['criterion']}: "
                        f"AI={disagreement['ai']} "
                        f"Human={disagreement['human']} "
                        f"Delta={disagreement['error']}"
                    )

    else:
        print("No matching transcripts found between JSON and CSV.")


if __name__ == "__main__":
    run_evaluation()