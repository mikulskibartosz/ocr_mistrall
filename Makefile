.PHONY: format generate-baml

format:
	poetry run black .

generate-baml:
	poetry run baml-cli generate