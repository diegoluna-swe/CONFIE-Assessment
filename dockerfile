FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy dependency configuration files
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry (or pip if you extract them), skipping root package build
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

VOLUME /app/results

# Copy the rest of the project files (including src/)
COPY . .

CMD ["python", "src/main.py"]