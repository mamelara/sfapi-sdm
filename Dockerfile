FROM python:3.8-buster

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=${PATH}:/etc/poetry/bin

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . /app

CMD ["uvicorn", "sfapi_sdm.main:app", "--host", "0.0.0.0", "--port", "8000"]
