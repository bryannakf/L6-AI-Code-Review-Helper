FROM mcr.microsoft.com/dotnet/sdk:8.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python3-venv python3-full nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend /app/backend
COPY frontend /app/frontend

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/backend/requirements.txt \
    && cd /app/frontend && npm install

WORKDIR /app/backend
EXPOSE 5000

CMD ["sh", "-c", "/opt/venv/bin/gunicorn --bind 0.0.0.0:${PORT:-5000} app:app"]
