FROM python:3.13-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir inside container
WORKDIR /app

# Install dependencies first (better layer caching)
COPY src/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY src/ml/ ./ml

# Copy all api source code
COPY src/api/ .

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
