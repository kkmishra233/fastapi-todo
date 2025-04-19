FROM python:3.13-slim AS origin
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"

FROM origin AS pre-build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
RUN uv run opentelemetry-bootstrap -a install
COPY . .

FROM origin AS runtime
WORKDIR /app
COPY --from=pre-build /app /app
EXPOSE 8080
ENV OTEL_EXPORTER_OTLP_ENDPOINT=0.0.0.0:4317
CMD uv run opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter console \
    --service_name fast-api-todo \
    --exporter_otlp_endpoint ${OTEL_EXPORTER_OTLP_ENDPOINT} \
    uvicorn main:app --host 0.0.0.0 --port 8080