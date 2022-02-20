FROM python:3.9.6-alpine

WORKDIR /usr/src/data

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
