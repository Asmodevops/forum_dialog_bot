FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install uv==0.7.6

COPY ./infrastructure/pyproject.toml ./infrastructure/uv.lock /app/infrastructure/
WORKDIR /app/infrastructure
RUN uv sync

COPY ./dialog_bot/pyproject.toml ./dialog_bot/uv.lock /app/dialog_bot/
WORKDIR /app/dialog_bot
RUN uv sync

COPY ./infrastructure /app/infrastructure
COPY ./dialog_bot /app/dialog_bot
