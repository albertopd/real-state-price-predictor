# Starts from the python 3.10 official docker image
FROM python:3.13-slim

# Update OS packages to address vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Create a folder "app" at the root of the image
RUN mkdir /app

# Define /app as the working directory
WORKDIR /app

# Copy all the files in the current directory in /app
COPY . /app

# Update pip
RUN pip install --upgrade pip

# Install dependencies from "requirements.txt"
RUN pip install -r requirements.txt

# Expose the default port (useful for documentation and local development)
EXPOSE 8000

# Run the app with dynamic port (Render sets $PORT) and set host to 0.0.0.0 to make it run on the container's network
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
