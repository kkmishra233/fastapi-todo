FROM python:3.13-slim AS origin
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"

FROM origin AS pre-build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM origin AS runtime
WORKDIR /app
COPY --from=pre-build /app /app
EXPOSE 8080
CMD uv run uvicorn main:app --host 0.0.0.0 --port 8080