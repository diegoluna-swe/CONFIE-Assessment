# Call Grading & Evaluation Pipeline

Automated LLM-driven QA grading system for customer service transcripts using Google GenAI, Pydantic validation, and Docker containerization.
[Technical assessment]

## Architecture & Tech Stack

- **Language:** Python 3.13
- **LLM Provider:** Google GenAI (`gemini-3.1-flash`) with structured JSON parsing via Pydantic schemas.
- **Dependency Management:** Poetry (`package-mode = false`).
- **Containerization:** Docker & GNU Make for reproducible execution.

---

## Prerequisites

- Docker Desktop installed and running.
- A valid Google Gemini API key.

---

## Setup & Configuration

1. Clone the repository and navigate to the root directory.
2. Configure your environment variables by creating a `.env` file inside the `src/` directory with your API key:

```env
GEMINI_API_KEY=your_actual_api_key_here

```

---

## Execution Commands

The project uses a `Makefile` to streamline container builds, evaluation runs, and metric checks.

- **Build the Docker container:**

```bash
make build

```

- **Run the evaluation pipeline** (grades all transcripts and outputs to `results/grades.json`):

```bash
make run

```

- **Run calibration metrics** (evaluates exact match accuracy and MAE against `labels.csv` for C001–C015):

```bash
make metrics

```

---

## Time Tracking & Notes

- **Active Coding Time:** ~3.5 hours.
- **Elapsed Time:** ~4.5 hours (accounted for initial GitHub CLI authentication setup, Docker environment debugging, and a scheduled lunch break).
