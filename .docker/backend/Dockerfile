FROM python:3.10.7-slim-bullseye

LABEL version="1.0.0"
LABEL author="luizfelipevbll@gmail.com"

RUN addgroup --system app && adduser --system app --ingroup app

ENV CODE=/code/
RUN mkdir -p $CODE
RUN mkdir -p $CODE/book_review/static
RUN mkdir -p $CODE/book_review/media

WORKDIR $CODE

RUN apt-get update

RUN apt-get install -y \
    build-essential \
    apt-transport-https \
    libpq-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    ca-certificates

COPY . .

RUN chmod +x .docker/backend/entrypoint.sh

RUN pip install -U pip wheel setuptools
RUN pip install poetry==1.2.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main --no-interaction --no-ansi

RUN chown -R app:app .

USER app
