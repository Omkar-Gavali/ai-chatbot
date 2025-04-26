# backend/Dockerfile
FROM python:3.10-slim

# 1. Set the working directory
WORKDIR /app

# 2. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy everything: code, data, and pre-built vectors
COPY . .

# 4. Expose and run
ENV PORT=8080
EXPOSE 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
