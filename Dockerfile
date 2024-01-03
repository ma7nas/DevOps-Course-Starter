FROM python:3.11-buster as base

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
COPY . /opt/todoapp/
WORKDIR /opt/todoapp
ENV PATH=/opt/poetry/bin:$PATH
RUN poetry install
RUN poetry update
ENV WEBAPP_PORT=8000
EXPOSE ${WEBAPP_PORT}
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0", "todo_app.app:create_app()"]


FROM base as development



FROM base as production