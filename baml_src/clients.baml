// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> Mistral {
  provider "openai-generic"
  options {
    base_url "https://api.mistral.ai/v1"
    model "open-mistral-7b"
    api_key env.MISTRAL_API_KEY
  }
}

