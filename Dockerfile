FROM python:3.9-alpine

MAINTAINER austinstevesk

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


RUN pip3 install -r requirements.txt

CMD uvicorn app.app.main:app --reload 0.0.0.0:8000

