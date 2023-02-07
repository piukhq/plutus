FROM ghcr.io/binkhq/python:3.10-pipenv

WORKDIR /
ADD . .
RUN pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["python", "consumer.py"]
