from fastapi import FastAPI
from pydantic import BaseModel

from app.services.llm_service import (
    generate_response,
    generate_response_with_instructions,
)
app = FastAPI()


class ChatRequest(BaseModel):
    prompt: str


@app.post("/api/chat")
def chat(request: ChatRequest):

    answer = generate_response(
        request.prompt
    )

    return {
        "answer": answer
    }


@app.post("/api/chat/instructions")
def chat_with_instructions(request: ChatRequest):

    answer = generate_response_with_instructions(
        request.prompt
    )

    return {
        "answer": answer
    }

from app.schemas.conversation import ConversationRequest

from app.services.llm_service import (
    generate_conversation_response,
)

@app.post("/api/chat/conversation")
def chat_conversation(
    request: ConversationRequest
):

    messages = [
        message.model_dump()
        for message in request.messages
    ]

    answer = generate_conversation_response(
        messages
    )

    return {
        "answer": answer
    }


from fastapi import HTTPException

from app.schemas.chat import ChatResponse

from app.services.llm_service import (
    generate_safe_response,
)

@app.post(
    "/api/chat/safe",
    response_model=ChatResponse,
)
def safe_chat(request: ChatRequest):

    try:

        answer = generate_safe_response(
            request.prompt
        )

        return ChatResponse(
            answer=answer
        )

    except RuntimeError:

        raise HTTPException(
            status_code=502,
            detail="LLM service is currently unavailable",
        )

from fastapi.responses import StreamingResponse

from app.services.llm_service import generate_stream


@app.post("/api/chat/stream")
def stream_chat(request: ChatRequest):

    return StreamingResponse(
        generate_stream(request.prompt),
        media_type="text/plain",
    )


from app.schemas.restaurant_request import RestaurantRequest
from app.schemas.restaurant import RestaurantInfo

from app.services.llm_service import (
    generate_structured_restaurant,
)

@app.post(
    "/api/chat/structured",
    response_model=RestaurantInfo,
)
def structured_chat(
    request: RestaurantRequest,
):

    result = generate_structured_restaurant(
        restaurant_name=request.restaurant_name,
        cuisine=request.cuisine,
    )

    return result


from app.schemas.order import OrderInfo
from app.schemas.order_request import OrderExtractionRequest

from app.services.llm_service import extract_order


@app.post(
    "/api/chat/extract-order",
    response_model=OrderInfo,
)
def extract_order_endpoint(
    request: OrderExtractionRequest,
):

    result = extract_order(request.text)

    return result

from app.services.llm_service import chat_with_tools

@app.post("/api/chat/tools")
def chat_tools(request: ChatRequest):

    answer = chat_with_tools(
        request.prompt
    )

    return {
        "answer": answer
    }

from app.services.llm_service import chat_with_multiple_tools

@app.post("/api/chat/multi-tools")
def chat_multiple_tools(request: ChatRequest):

    answer = chat_with_multiple_tools(request.prompt)

    return {
        "answer": answer
    }

from app.services.llm_service import chat_with_safe_tools

@app.post("/api/chat/safe-tools")
def chat_safe_tools(request: ChatRequest):

    answer = chat_with_safe_tools(request.prompt)

    return {
        "answer": answer
    }

from app.services.llm_service import chat_with_database_tool

@app.post("/api/chat/db-tools")
def chat_database_tool(request: ChatRequest):

    answer = chat_with_database_tool(request.prompt)

    return {
        "answer": answer
    }


class SecureChatRequest(BaseModel):
    prompt: str
    user_id: int


from app.services.llm_service import chat_with_tool_chain

@app.post("/api/chat/tool-chain")
def chat_tool_chain(request: SecureChatRequest):

    answer = chat_with_tool_chain(
        request.prompt,
        request.user_id,
    )

    return {
        "answer": answer
    }


from app.schemas.embedding import EmbeddingRequest
from app.services.embedding_service import create_embedding


@app.post("/api/embeddings")
def create_text_embedding(
    request: EmbeddingRequest,
):

    embedding = create_embedding(request.text)

    return {
        "text": request.text,
        "dimensions": len(embedding),
        "embedding": embedding,
    }