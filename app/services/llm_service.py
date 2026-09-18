import os

from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_response(prompt: str) -> str:

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text

def generate_response_with_instructions(prompt: str) -> str:

    response = client.responses.create(
        model="gpt-5-mini",

        instructions=(
            "You are a senior backend engineer. "
            "Explain technical concepts using simple examples. "
            "When possible, compare concepts with Django."
        ),

        input=prompt,
    )

    return response.output_text

def generate_conversation_response(
    messages: list[dict]
) -> str:

    response = client.responses.create(
        model="gpt-5-mini",
        input=messages,
    )

    return response.output_text


from openai import OpenAIError


def generate_safe_response(prompt: str) -> str:

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt,
        )

        return response.output_text

    except OpenAIError as exc:

        raise RuntimeError(
            "Failed to generate LLM response"
        ) from exc
    

def generate_stream(prompt: str):

    stream = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        stream=True,
    )

    for event in stream:

        if event.type == "response.output_text.delta":
            yield event.delta

from app.schemas.restaurant import RestaurantInfo

def generate_structured_restaurant(
    restaurant_name: str,
    cuisine: str,
) -> RestaurantInfo:

    response = client.responses.parse(
        model="gpt-5-mini",

        input=[
            {
                "role": "developer",
                "content": (
                    "You are a restaurant information assistant. "
                    "Return restaurant information using the "
                    "provided structured format."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Restaurant name: {restaurant_name}\n"
                    f"Cuisine: {cuisine}"
                ),
            },
        ],

        text_format=RestaurantInfo,
    )

    return response.output_parsed