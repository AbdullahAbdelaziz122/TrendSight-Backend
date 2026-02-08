# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build tools
RUN pip install --no-cache-dir build

COPY pyproject.toml . 

COPY app ./app

# Build the wheels
RUN pip wheel --no-cache-dir --wheel-dir /wheels .



# Stage 2: Runner
FROM python:3.10-slim AS runner

WORKDIR /app

# Install runtime system libraries (libpq is needed for Postgres drivers)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install all wheels (dependencies + app)
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# Copy Alembic configuration AND the migrations folder
COPY alembic.ini .
COPY alembic ./alembic 


# Create non-root user
RUN useradd -m -u 1000 fastapi && \
    chown -R fastapi:fastapi /app

USER fastapi

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]