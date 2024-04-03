FROM ghcr.io/binkhq/python:3.10

WORKDIR /app

RUN pip install poetry
RUN poetry self add "poetry-dynamic-versioning[plugin]"
RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install

CMD ["python", "consumer.py"]
