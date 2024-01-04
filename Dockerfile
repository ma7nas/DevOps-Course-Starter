FROM python:3.11-buster as base

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH=/opt/poetry/bin:$PATH
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . /opt/todoapp/
WORKDIR /opt/todoapp
ENV WEBAPP_PORT=8000
EXPOSE ${WEBAPP_PORT}
RUN poetry install --without dev

FROM base as development
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

FROM base as production
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]