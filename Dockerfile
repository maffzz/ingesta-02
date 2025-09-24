FROM python:3.11-slim

# System deps (optional, helpful for PyMySQL)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ingesta.py ./

# Default command
CMD ["python", "ingesta.py"]
