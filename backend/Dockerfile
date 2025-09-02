FROM python:3.12-slim

WORKDIR /app/backend

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /app/backend/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /app/backend

CMD [ "poetry", "run", "fastapi", "run", "src/api.py", "--port", "80" ]
