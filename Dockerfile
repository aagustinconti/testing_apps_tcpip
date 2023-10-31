FROM python:3.10

COPY ./poetry.lock
COPY ./pyproject.toml

RUN pip install poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install

COPY .app /

CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0