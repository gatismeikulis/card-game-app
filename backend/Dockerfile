FROM python:3.12-slim

# Prevents Python from writing .pyc files (saves space, faster builds)
ENV PYTHONDONTWRITEBYTECODE=1 
# Makes Python output appear immediately in Docker logs (no buffering)
ENV PYTHONUNBUFFERED=1

RUN pip install uv

WORKDIR /app

# Copy dependencies and lock files, install dependencies
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen

# Copy the rest of your project
COPY . /app/

# Documents that the container will listen on port 8000 (Django's default port)
EXPOSE 8000

# Make entrypoint executable (adds execution permissions)
RUN chmod +x /app/docker-entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["sh","/app/docker-entrypoint.sh"]

