FROM python:3.11.4

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
    && apt-get install -y libpq-dev gcc python3-dev musl-dev git ffmpeg xvfb wkhtmltopdf

# install dependencies
RUN pip install --upgrade pip setuptools wheel
COPY . .
RUN pip install -r requirements.txt
