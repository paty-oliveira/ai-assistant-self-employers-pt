FROM python:3.12-slim AS builder

WORKDIR /app/frontend

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /app/frontend/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

FROM python:3.12-slim

WORKDIR /app/frontend

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app/frontend

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0" ]
