FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image


# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
ADD pyproject.toml uv.lock /app
RUN uv sync --frozen

ADD . /app
EXPOSE 8123

CMD ["uv", "run", "uvicorn", "submerged.web:app", "--host", "0.0.0.0", "--port", "8123"]