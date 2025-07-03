FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install uv==0.7.6

COPY ./infrastructure/pyproject.toml ./infrastructure/uv.lock /app/infrastructure/
WORKDIR /app/infrastructure
RUN uv sync

COPY ./fix-user-service/pyproject.toml ./fix-user-service/uv.lock /app/fix-user-service/
WORKDIR /app/fix-user-service
RUN uv sync

COPY ./infrastructure /app/infrastructure
COPY ./fix-user-service /app/fix-user-service
