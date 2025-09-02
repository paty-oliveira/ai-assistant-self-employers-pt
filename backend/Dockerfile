# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app/backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /app/backend/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

# Production stage
FROM python:3.12-slim

WORKDIR /app/backend

COPY --from=builder app/backend /usr/local

COPY . /app/backend

CMD [ "poetry", "run", "fastapi", "run", "src/api.py", "--port", "80" ]
