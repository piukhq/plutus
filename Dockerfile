FROM ghcr.io/binkhq/python:3.10-pipenv

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .

RUN poetry build

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["python", "consumer.py"]
