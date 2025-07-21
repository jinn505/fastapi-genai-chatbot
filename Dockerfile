FROM python:3.11-slim

WORKDIR /app

# ✅ Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-qdrant.sh /wait-for-qdrant.sh
RUN chmod +x /wait-for-qdrant.sh

CMD ["/wait-for-qdrant.sh", "qdrant", "6333", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
