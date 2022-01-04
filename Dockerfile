FROM python:3.9-alpine

COPY requirements.txt /tmp/
RUN pip insall --upgrade pip
RUN pip install -r /tmp/reqirements.txt

RUN mkdir -p /src
COPY src/ /src/
COPY tests/ /tests/

WORKDIR /src
