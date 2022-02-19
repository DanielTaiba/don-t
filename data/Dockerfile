FROM python:3.8.12-bullseye

WORKDIR /usr/src/data

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
