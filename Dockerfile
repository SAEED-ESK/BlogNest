FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -i https://mirror-pypi.runflare.com/simple --upgrade pip
RUN pip install -i https://mirror-pypi.runflare.com/simple -r requirements.txt

COPY ./core /app/