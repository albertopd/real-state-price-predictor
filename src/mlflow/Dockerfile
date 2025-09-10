FROM ghcr.io/mlflow/mlflow:v3.3.2

WORKDIR /opt/project

# Install dependencies
COPY src/mlflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/mlflow ./src/mlflow