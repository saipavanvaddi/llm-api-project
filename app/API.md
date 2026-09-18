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

Answer a prompt using function calling. Only `get_order_status` results are handled — the endpoint advertises both order tools (see the shared `order_tools` list in `app/services/llm_service.py`), but its handler ignores any other tool call by name.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "Where is my order 103?"
}
```

**Response `200`** — model called `get_order_status`

```json
{
  "answer": "Your order #103 is currently out for delivery."
}
```

**Response `200`** — model called `get_order_items` instead ⚠️

Because the model can also see `get_order_items` (it shares the `order_tools` schema list with `/api/chat/multi-tools`), a prompt like `"What items are in order 101?"` can lead the model to call `get_order_items`. `chat_with_tools()` only recognizes `get_order_status` by name and silently drops any other tool call, so no tool output is sent back and the endpoint returns an empty answer:

```json
{
  "answer": ""
}
```

Known order IDs (see `app/tools/order_tools.py`): `101` Preparing, `102` Ready for pickup, `103` Out for delivery, `104` Delivered. Any other ID returns `{"order_id": <id>, "status": "Order not found"}`.

---

## POST /api/chat/multi-tools

Answer a prompt using function calling, choosing between two tools — `get_order_status` and `get_order_items` — based on the prompt. Both tools take the same `order_id: integer` argument.

**Request body**

| Field  | Type   | Required |
|--------|--------|----------|
| prompt | string | yes      |

```json
{
  "prompt": "What items are in order 103?"
}
```

**Response `200`**

| Field  | Type   |
|--------|--------|
| answer | string |

**Case 1 — model calls `get_order_status`**

Request:

```json
{
  "prompt": "What is the status of order 103?"
}
```

Tool call: `get_order_status(order_id=103)` → `{"order_id": 103, "status": "Out for delivery"}`

Response:

```json
{
  "answer": "Order 103 is out for delivery."
}
```

**Case 2 — model calls `get_order_items`, order found**

Request:

```json
{
  "prompt": "What items are in order 101?"
}
```

Tool call: `get_order_items(order_id=101)` → `{"order_id": 101, "items": [{"name": "Chicken Biryani", "quantity": 2}, {"name": "Coke", "quantity": 1}]}`

Response:

```json
{
  "answer": "Order 101 contains:\n- Chicken Biryani — 2\n- Coke — 1"
}
```

**Case 3 — model calls `get_order_items`, order not found**

Request:

```json
{
  "prompt": "What items are in order 999?"
}
```

Tool call: `get_order_items(order_id=999)` → `{"order_id": 999, "items": [], "message": "Order not found"}`

Response (wording varies — the model summarizes the tool output, it isn't returned verbatim):

```json
{
  "answer": "I couldn't find order 999 — it doesn't exist in our system."
}
```

**Case 4 — no tool call needed**

For a prompt that doesn't relate to an order (e.g. a general question), the model answers directly without calling either tool:

```json
{
  "prompt": "What is your refund policy in general?"
}
```

```json
{
  "answer": "I don't have a specific refund policy to share — that depends on the vendor or store you purchased from..."
}
```

**Available tools**

| Tool               | Arguments          | Description                             | Sample IDs   |
|---------------------|--------------------|------------------------------------------|--------------|
| `get_order_status`  | `order_id: integer`| Current status of a food delivery order   | `101`–`104`  |
| `get_order_items`   | `order_id: integer`| Line items in a food delivery order       | `101`, `102` |

Sample data lives in `app/tools/order_tools.py`. Note the two tools currently use different mock datasets: `get_order_status` knows orders `101`–`104`, while `get_order_items` only knows `101` and `102` — asking for the status of `101`/`102` and the items of `103`/`104` are both valid requests, but only one of the two tools will have data for the full `101`–`104` range.

---

## Notes

- `/api/chat`, `/api/chat/instructions`, `/api/chat/conversation`, `/api/chat/structured`, `/api/chat/extract-order`, `/api/chat/tools`, and `/api/chat/multi-tools` do not currently catch OpenAI API errors — a failure upstream (bad input, rate limit, etc.) returns an unhandled `500 Internal Server Error`. `/api/chat/safe` is the only endpoint with graceful error handling (`502`); the same pattern can be applied to the others.
- Validation errors (e.g. missing `prompt` field) return FastAPI's default `422 Unprocessable Entity` with a `detail` array describing the offending field.
- `/api/chat/tools` and `/api/chat/multi-tools` share the same `order_tools` tool-schema list in `app/services/llm_service.py`. `/api/chat/tools`'s handler (`chat_with_tools`) only processes `get_order_status` calls, so if a prompt leads the model to call `get_order_items` there instead, the tool call is silently dropped and the endpoint returns `{"answer": ""}`. See the `/api/chat/tools` section above.
