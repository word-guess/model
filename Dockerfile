FROM python:3.10-bullseye as fetcher

WORKDIR /app

COPY ./.env ./get-model.py /app/

ARG MODEL_URL
ENV MODEL_URL $MODEL_URL
RUN MODEL_URL=$MODEL_URL python3 /app/get-model.py


FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y python-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY --from=fetcher /app/content/model.bin /app/content/
COPY ./main.py /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
