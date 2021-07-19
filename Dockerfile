FROM python:3.8-buster

WORKDIR /app

RUN apt-get update && \
    apt-get -y install python3-lxml

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
