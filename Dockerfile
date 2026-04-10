ARG APP_HOME=/app

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR ${APP_HOME}

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  UV_COMPILE_BYTECODE=1 \
  UV_LINK_MODE=copy \
  UV_PYTHON_DOWNLOADS=0

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen

FROM python:3.13-slim-bookworm AS runtime

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

ENV \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/app/.venv/bin:$PATH"

RUN useradd --create-home --shell /usr/sbin/nologin appuser
USER appuser

COPY --from=builder ${APP_HOME} ${APP_HOME}

CMD ["python", "main.py"]
