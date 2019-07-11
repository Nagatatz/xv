FROM python:3.7

ARG PROJECT_ENV

ENV PROJECT_ENV=${PROJECT_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=0.12.11

RUN pip install "poetry==$POETRY_VERSION"

RUN mkdir /code
WORKDIR /code
COPY src/pyproject.toml /code/pyproject.toml
COPY src/poetry.lock /code/poetry.lock

# Project initialization:
RUN poetry config settings.virtualenvs.create false \
  && poetry install $(test "$PROJECT_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /code/