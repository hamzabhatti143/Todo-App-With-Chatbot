# Todo Backend

FastAPI backend application for the Todo full-stack web application.

## Tech Stack

- **FastAPI 0.115.6** - Modern Python web framework
- **SQLModel 0.0.22** - SQL databases with Python type hints
- **PostgreSQL** - Relational database
- **Alembic 1.14.0** - Database migrations
- **python-jose 3.3.0** - JWT token handling
- **Passlib 1.7.4** - Password hashing
- **Uvicorn 0.34.0** - ASGI server

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- pip package manager

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-here-min-32-chars
CORS_ORIGINS=http://localhost:3000
```

### Database Setup

1. Create the database:
```bash
createdb todo_db
```

2. Run migrations:
```bash
alembic upgrade head
```

### Development

Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

### Type Checking

Run mypy for type checking:
```bash
mypy app/
```

### Code Quality

Run ruff for linting and formatting:
```bash
ruff check .
ruff format .
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models/          # SQLModel database models
│   ├── routes/          # API route handlers
│   └── schemas/         # Pydantic schemas
├── alembic/             # Database migrations
├── tests/               # Test files
└── requirements.txt     # Python dependencies
```

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /health` - Health check endpoint

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Database Models

### Task
- `id`: UUID (primary key)
- `title`: String (max 200 chars)
- `description`: String (optional, max 1000 chars)
- `completed`: Boolean (default: False)
- `user_id`: UUID (foreign key to User)
- `created_at`: DateTime
- `updated_at`: DateTime

### User
- `id`: UUID (primary key)
- `email`: String (unique)
- `hashed_password`: String
- `created_at`: DateTime

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | - |
| `BETTER_AUTH_SECRET` | Secret for Better Auth integration | - |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | - |
| `JWT_ALGORITHM` | Algorithm for JWT encoding | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `DEBUG` | Debug mode | `True` |

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- CORS middleware configured for frontend origin
- SQL injection protection via SQLModel/SQLAlchemy
- Input validation with Pydantic schemas

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
