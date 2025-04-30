# OCR Contracts

## Zmiana API Mistral na Ollama

W pliku `baml_src/clients.baml` zmieniamy:

```
client<llm> Mistral {
  provider "openai-generic"
  options {
    base_url "https://api.mistral.ai/v1"
    model "open-mistral-7b"
    api_key env.MISTRAL_API_KEY
  }
}
```

na:

```
client<llm> MyClient {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model mistral-7b
  }
}
```

## Instalacja

```bash
poetry install
```

Tworzymy plik `.env` kopiując zawartość pliku `.env.example` i wklejając klucz API z Mistrala (nawet jeśli używamy Ollamy będzie potrzebny do OCR).

## Uruchomienie (lokalnie)

```bash
poetry run fastapi dev api.py
```

## Testowanie lokalnie

```bash
poetry run python send_file.py /path/to/your/file.pdf
```

## Budowanie obrazu Dockera

```bash
docker build -t ocr-contracts .
```

## Uruchamianie Dockera

```bash
docker run -d -e MISTRAL_API_KEY=<klucz-api-mistrala> -p 8080:8080 ocr-contracts
```

## Zatrzymywanie Dockera

```bash
docker ps
docker stop <id-kontenera>
```

## Docker Compose

### Budowanie obrazu Dockera

```bash
docker compose build
```

### Uruchomienie obu usług

```bash
MISTRAL_API_KEY=<klucz-api-mistrala> docker compose up -d
```

### Wyłączenie obu usług

```bash
docker compose down
```
