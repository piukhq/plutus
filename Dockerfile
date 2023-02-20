FROM ghcr.io/binkhq/python:3.10

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["python", "consumer.py"]
