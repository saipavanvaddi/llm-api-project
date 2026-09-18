llm-api-project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   └── services/
│       ├── __init__.py
│       └── llm_service.py
│
├── .env
├── .gitignore
└── requirements.txt


pip install fastapi uvicorn openai python-dotenv


uvicorn app.main:app --reload