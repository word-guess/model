FROM python:3.10-bullseye as fetcher

WORKDIR /home/app

COPY ./get-model.py /home/app/

ARG MODEL_URL
ENV MODEL_URL $MODEL_URL
RUN MODEL_URL=$MODEL_URL python3 /home/app/get-model.py


FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y python-dev

WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir -r /home/app/requirements.txt

COPY --from=fetcher /home/app/content/model.bin /home/app/content/
COPY ./main.py /home/app/

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
