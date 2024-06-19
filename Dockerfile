FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY . . 

RUN chmod +x entrypoint.sh

RUN pip install poetry

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]

CMD poetry run uvicorn --host 0.0.0.0 cinematch_back.app:app
