FROM python:3.10-alpine

COPY ../../../src /waiter/src/
COPY ../../../deployment /waiter/deployment/

WORKDIR waiter/src

RUN pip install -r entrypoints/fastapi/requirements.txt

CMD ["hypercorn", "entrypoints.fastapi.app:app", "--bind", "0.0.0.0:8000", "-w", "4"]
