.PHONY: format generate-baml

format:
	poetry run black .

generate-baml:
	poetry run baml-cli generate

run:
	poetry run fastapi dev api.py

run-prod:
	poetry run fastapi run api.py --host 0.0.0.0 --port 8080
