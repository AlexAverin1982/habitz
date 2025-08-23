FROM python:3.13-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir /app/static

RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
