FROM python:3.12.7-alpine3.19
LABEL maintainer="nazargorodyko@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
