import config
from huggingface_hub import InferenceClient

MODELS = config.HF_MODELS


def generate_response(
    prompt: str,
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> str:

    if not config.HF_API_KEY:
        return "Error: HF_API_KEY not found."

    last_error = None

    for model in MODELS:
        try:
            client = InferenceClient(
                model=model,
                token=config.HF_API_KEY,
            )

            response = client.chat_completion(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            return content if content else ""

        except Exception as e:
            last_error = e

    return f"Hugging Face Error: {last_error}"