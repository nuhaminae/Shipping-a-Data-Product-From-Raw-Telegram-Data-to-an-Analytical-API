# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy files into container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements-docker.txt

# Load environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for FastAPI
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "scripts.api.main:app", "--host", "0.0.0.0", "--port", "8000"]