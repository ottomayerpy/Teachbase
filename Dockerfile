FROM python:3.10


WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt
COPY . .
