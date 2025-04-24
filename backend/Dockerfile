
# Dockerfile
FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app

# Expose the port (Cloud Run uses $PORT)
ENV PORT 8080
EXPOSE 8080

# Run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
