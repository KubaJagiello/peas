FROM python:3.12-slim

# install make
RUN apt-get update && apt-get install -y \
    make \
    curl \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# installa poetry

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# RUN poetry install
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "dev", "peas_app/api/app.py", "--host", "0.0.0.0"]
