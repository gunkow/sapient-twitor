FROM python:3.7.6-alpine3.11
LABEL maintainer = "gunkow@gmail.com"
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY  . ./api

RUN apk update && apk upgrade \
     && apk add postgresql-dev gcc python3-dev musl-dev libc-dev make \
    && pip install -r api/requirements.txt
