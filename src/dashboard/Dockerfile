FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY src/dashboard/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the dashboard source code
COPY src/dashboard/app ./src/dashboard/app

# Expose Streamlit port
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "src/dashboard/app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
