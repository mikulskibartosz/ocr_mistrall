FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false

RUN poetry install --only main

COPY . .

EXPOSE 8080

CMD ["poetry", "run", "fastapi", "run", "api.py", "--host", "0.0.0.0", "--port", "8080"]
