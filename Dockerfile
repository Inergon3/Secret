FROM python:3.12.4-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo '#!/bin/sh\n\
echo "Waiting for PostgreSQL to be ready..."\n\
while ! pg_isready -h db -U inergon -d db_secret; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
\n\
echo "Running migrations..."\n\
alembic upgrade head\n\
\n\
echo "Starting application..."\n\
cd /app && uvicorn main:app --host 0.0.0.0 --port 8000' > /app/start.sh && \
chmod +x /app/start.sh

CMD ["/app/start.sh"]
