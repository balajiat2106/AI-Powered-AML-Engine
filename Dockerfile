FROM python:3.11-slim

WORKDIR /app

# Install OS utilities (e.g. for psycopg2 build or machine learning packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose PYTHONPATH so that uvicorn can detect the "src" module correctly 
ENV PYTHONPATH="/app"

EXPOSE 8000

# Run API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
