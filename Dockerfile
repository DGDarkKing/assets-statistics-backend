FROM python:3.12.0-slim
LABEL authors="Danila"

ENV PYTHONUNBUFFERED=1
WORKDIR project

ARG POETRY_VERSION
ENV POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY poetry.lock pyproject.toml ./
RUN poetry cache clear . --all \
    && poetry install

COPY ./src/ ./
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]