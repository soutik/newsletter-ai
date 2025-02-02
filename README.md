# AI-Powered Newsletter Generator

A system that curates personalized newsletters using LLMs, vector databases, and news APIs. Users subscribe to topics, and the system generates weekly summaries of relevant articles.

## Features
- **Personalized Newsletters**: Tailored to user-selected topics (e.g., AI, Climate).
- **LLM Summarization**: GPT-3.5/4 for article summaries and ranking.
- **Vector Database**: Qdrant for deduplication and semantic filtering.
- **User Management**: PostgreSQL database for user preferences.
- **Simple Web UI**: Flask frontend for signups.

## Prerequisites
- Python 3.9+
- Docker and Docker Compose
- API Keys:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [NewsAPI Key](https://newsapi.org/register)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/newsletter-ai.git
cd newsletter-ai
```

2. Set Up Backend

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

# Install dependencies
```bash
pip install -r requirements.txt
```

3. Set Up Frontend

```bash
# Install Flask (if not already installed)
pip install flask requests
```

4. Environment Variables

Create a .env file in the project root:

```bash
# .env
OPENAI_API_KEY="your_openai_key"
NEWSAPI_KEY="your_newsapi_key"

# PostgreSQL (matches docker-compose.yml)
POSTGRES_USER="newsletterai"
POSTGRES_PASSWORD="yourpassword"
POSTGRES_DB="newsletterai"

# Email sending (for gmail get the app token instead of your password)
SENDER_EMAIL="emailID"
SENDER_PASSWORD="password"
```

# Running the System

1. Start Databases

```bash
docker-compose up -d  # Starts PostgreSQL and Qdrant
```

2. Run Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

3. Run Frontend (Flask)

```bash
cd frontend
python app.py  # Runs on http://localhost:5000
```

# Testing with Sample Data

1. Create Test Users

```bash
python scripts/init_test_data.py
```

2. Trigger Newsletter Generation

```bash
python app.py  # Main workflow
```

3. Verify Output

Check generated HTML files in the project root (output_*.html)
Validate database entries:
```bash
docker exec -it newsletter-ai-postgres-1 psql -U newsletterai -d newsletterai -c "SELECT * FROM users;"
```

# Configuration

### Environment Variables

| Variable            | Description                        |
|---------------------|------------------------------------|
| `OPENAI_API_KEY`     | Required for GPT summarization     |
| `NEWSAPI_KEY`        | News article sourcing             |
| `POSTGRES_*`         | PostgreSQL credentials (Docker)   |

### Docker Services

- **PostgreSQL**: `postgres:15` @ `localhost:5432`
- **Qdrant**: `qdrant/qdrant` @ `localhost:6333`

Project Structure

```bash
/newsletter-ai
├── backend/               # FastAPI backend
│   ├── main.py           # API endpoints
│   └── requirements.txt
├── frontend/             # Flask frontend
│   ├── app.py
│   └── templates/        # HTML templates
├── docker-compose.yml    # Database config
├── app.py                # Main newsletter workflow
├── models/               # Database models
├── services/             # Business logic
├── utils/                # Helper modules
└── scripts/              # Test/data scripts
```

# Troubleshooting

## Common Issues

### API Rate Limits:
NewsAPI free tier allows 100 requests/day
OpenAI: Monitor usage at https://platform.openai.com/usage
Docker Errors:
```bash
# Restart containers
docker-compose down && docker-compose up -d
```

### LLM Hallucinations:
Add `temperature=0.3` to reduce creativity
Implement summary validation (see `utils/llm_handler.py`)

FastAPI: http://localhost:8000/docs (API documentation)
PostgreSQL logs: `docker logs newsletter-ai-postgres-1`
Qdrant: `docker logs newsletter-ai-qdrant-1`
