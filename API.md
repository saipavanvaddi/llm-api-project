# API Reference

Base URL: `http://localhost:8000`

All endpoints are `POST` requests with a JSON body (except `/api/chat/stream`, which returns a plain-text stream) and use the `gpt-5-mini` model under the hood.

---

## POST /api/chat

Generate a plain response to a single prompt.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "What is a REST API?"
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

```json
{
  "answer": "A REST API is..."
}
```

---

## POST /api/chat/instructions

Same as `/api/chat`, but the model is given fixed system instructions to answer as a senior backend engineer and compare concepts to Django where possible.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "What is a decorator?"
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

```json
{
  "answer": "A decorator is a callable that wraps another callable... (similar to a Django middleware)"
}
```

---

## POST /api/chat/conversation

Generate a response from a full multi-turn conversation history.

**Request body**

| Field    | Type      | Required |
|----------|-----------|----------|
| messages | Message[] | yes      |

`Message`

| Field   | Type   | Required |
|---------|--------|----------|
| role    | string | yes      |
| content | string | yes      |

```json
{
  "messages": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help you today?" },
    { "role": "user", "content": "What's FastAPI?" }
  ]
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

```json
{
  "answer": "FastAPI is a Python web framework for building APIs..."
}
```

---

## POST /api/chat/safe

Same as `/api/chat`, but wraps the LLM call in error handling and returns a clean `502` instead of an unhandled `500` if the OpenAI call fails.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "What is a REST API?"
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

```json
{
  "answer": "A REST API is..."
}
```

**Response `502`** — LLM call failed (e.g. upstream error, rate limit, invalid key)

```json
{
  "detail": "LLM service is currently unavailable"
}
```

---

## POST /api/chat/stream

Same as `/api/chat`, but streams the answer back as plain text chunks as they're generated, instead of waiting for the full response.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "Write a short poem about the ocean."
}
```

**Response `200`**

`Content-Type: text/plain` — a streamed sequence of text chunks (not JSON). Concatenating all chunks yields the full answer, e.g.:

```
The ocean stretches wide and blue...
```

---

## POST /api/chat/structured

Generate structured information about a restaurant, given its name and cuisine.

**Request body**

| Field           | Type   | Required |
|-----------------|--------|----------|
| restaurant_name | string | yes      |
| cuisine         | string | yes      |

```json
{
  "restaurant_name": "Olive Garden",
  "cuisine": "Italian"
}
```

**Response `200`** (`RestaurantInfo`)

| Field       | Type    |
|-------------|---------|
| name        | string  |
| cuisine     | string  |
| description | string  |
| rating      | float   |
| vegetarian  | boolean |

```json
{
  "name": "Olive Garden",
  "cuisine": "Italian",
  "description": "A casual dining chain serving classic Italian dishes like pasta, breadsticks, and salad.",
  "rating": 4.1,
  "vegetarian": false
}
```

---

## POST /api/chat/extract-order

Extract a structured food order (line items + total price) from free-form text.

**Request body**

| Field | Type   | Required |
|-------|--------|----------|
| text  | string | yes      |

```json
{
  "text": "I'd like 2 cheeseburgers at $8.50 each and a large fries for $3.00"
}
```

**Response `200`** (`OrderInfo`)

| Field | Type        |
|-------|-------------|
| items | OrderItem[] |
| total | float       |

`OrderItem`

| Field    | Type   |
|----------|--------|
| name     | string |
| quantity | int    |
| price    | float  |

```json
{
  "items": [
    { "name": "cheeseburger", "quantity": 2, "price": 8.50 },
    { "name": "large fries", "quantity": 1, "price": 3.00 }
  ],
  "total": 20.00
}
```

---

## POST /api/chat/tools

Answer a prompt using function calling: the model can call the `get_order_status` tool to look up a food delivery order by ID, and the answer is generated from the tool's result.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "Where is my order 103?"
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

```json
{
  "answer": "Your order #103 is currently out for delivery."
}
```

Known order IDs (see `app/tools/order_tools.py`): `101` Preparing, `102` Ready for pickup, `103` Out for delivery, `104` Delivered. Any other ID returns "Order not found".

---

## Notes

- `/api/chat`, `/api/chat/instructions`, `/api/chat/conversation`, `/api/chat/structured`, `/api/chat/extract-order`, and `/api/chat/tools` do not currently catch OpenAI API errors — a failure upstream (bad input, rate limit, etc.) returns an unhandled `500 Internal Server Error`. `/api/chat/safe` is the only endpoint with graceful error handling (`502`); the same pattern can be applied to the others.
- Validation errors (e.g. missing `prompt` field) return FastAPI's default `422 Unprocessable Entity` with a `detail` array describing the offending field.
