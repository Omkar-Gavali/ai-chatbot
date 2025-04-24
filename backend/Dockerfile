# backend/Dockerfile

# 1. Use a lightweight base image
FROM python:3.10-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements first (for layer caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY app/ ./app

# 6. Expose the port Cloud Run will route to
ENV PORT 8080
EXPOSE 8080

# 7. Launch the Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
