FROM apache/airflow:2.9.3

# Install git in a single RUN step and clean up cache
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install dependencies
COPY src/airflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY src/ml /opt/project/src/ml
COPY src/scrapers /opt/project/src/scrapers

# Copy dags
COPY src/airflow/dags /opt/airflow/dags

# Set Python path
ENV PYTHONPATH=/opt/project/src