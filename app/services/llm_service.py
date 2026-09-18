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


from app.schemas.order import OrderInfo


def extract_order(text: str) -> OrderInfo:

    response = client.responses.parse(
        model="gpt-5-mini",

        input=[
            {
                "role": "developer",
                "content": (
                    "Extract food order information from the "
                    "user's text. Calculate the total price."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],

        text_format=OrderInfo,
    )

    return response.output_parsed


import json

from app.tools.order_tools import get_order_status


order_tools = [
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Get the current status of a food delivery order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "The ID of the food order.",
                }
            },
            "required": ["order_id"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


# def chat_with_tools(user_message: str):

#     response = client.responses.create(
#         model="gpt-5-mini",
#         input=user_message,
#         tools=order_tools,
#     )
#     # At this point the model can request the tool.
#     # But our backend still needs to execute it.
#     return response

def chat_with_tools(user_message: str):

    response = client.responses.create(
        model="gpt-5-mini",
        input=user_message,
        tools=order_tools,
    )

    tool_outputs = []

    for item in response.output:

        if item.type == "function_call":

            if item.name == "get_order_status":

                arguments = json.loads(item.arguments)

                result = get_order_status(
                    arguments["order_id"]
                )

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result),
                })

    if tool_outputs:

        final_response = client.responses.create(
            model="gpt-5-mini",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=order_tools,
        )

        return final_response.output_text

    return response.output_text