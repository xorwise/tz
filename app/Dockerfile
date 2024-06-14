FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock .
RUN poetry install

COPY . .
