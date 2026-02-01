FROM python:3.12-slim

# Build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==2.2.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# COPY pyproject.toml poetry.lock README.md ./
# COPY src ./src
COPY . .

RUN poetry install

# Install Playwright system dependencies + browser
RUN poetry run playwright install-deps chromium
RUN poetry run playwright install chromium
# Set working directory to where manage.py lives
WORKDIR /app/src/cs2_webscraper_service/cs2_webscraper_django_app

# Create migrations, apply them, then start Django server
CMD poetry run python manage.py makemigrations && \
    poetry run python manage.py migrate && \
    poetry run python manage.py runserver 0.0.0.0:8000