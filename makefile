build:
	docker build -t transcript-evaluator .

run:
	docker run --rm --env-file src/.env -v "$(shell pwd)/results:/app/results" -v "$(shell pwd)/labels.csv:/app/labels.csv" transcript-evaluator

metrics:
	docker run --rm --env-file src/.env -v "$(shell pwd)/results:/app/results" -v "$(shell pwd)/labels.csv:/app/labels.csv" transcript-evaluator python src/evaluate_metrics.py

all: build run metrics