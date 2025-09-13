FROM apache/airflow:2.9.3

# Install dependencies
COPY src/airflow/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared code
COPY src/utils /opt/project/src/utils
COPY src/ml /opt/project/src/ml
COPY src/scrapers /opt/project/src/scrapers

# Copy dags
COPY src/airflow/dags /opt/airflow/dags

# Set Python path
ENV PYTHONPATH=/opt/project/src