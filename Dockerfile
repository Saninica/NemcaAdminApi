FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client libraries and build dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY req.txt .

RUN pip install --no-cache-dir -r req.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

ENV ENV=production

ENTRYPOINT ["/app/entrypoint.sh"]
