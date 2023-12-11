FROM python:3.10.13-slim

RUN pip install poetry

COPY ./poetry.lock /
COPY ./pyproject.toml /

RUN poetry config virtualenvs.in-project false && \
    poetry install --only=main --no-root

COPY ./app /app

CMD poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0