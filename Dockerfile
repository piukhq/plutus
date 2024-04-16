FROM ghcr.io/binkhq/python:3.10

ARG PIP_INDEX_URL
ARG APP_NAME
ARG APP_VERSION

WORKDIR /app

COPY . .

RUN pip install --no-cache ${APP_NAME}==$(echo ${APP_VERSION} | cut -c 2-)
