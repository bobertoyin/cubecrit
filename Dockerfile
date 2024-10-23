FROM python:3.10
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /cubecrit
COPY poetry.lock pyproject.toml ./
COPY /cubecrit/ ./cubecrit
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --only main
CMD ["poetry", "run", "flask", "--app", "cubecrit", "run", "--port", "3000", "--host", "0.0.0.0"]
