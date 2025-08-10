FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y

ADD ./requirements.txt /sources/requirements.txt
RUN pip install -r /sources/requirements.txt

WORKDIR /sources

ADD ./app /sources