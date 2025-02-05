# Use an official slim Python runtime as a parent image (now matching the project requirement)
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry globally
RUN pip install poetry

# Disable Poetry's virtual environment creation
ENV POETRY_VIRTUALENVS_CREATE=false

# Copy only dependency files to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies using Poetry (without dev dependencies and without installing the project itself)
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Expose the port that the application will run on
EXPOSE 8000

# Define the command to run the application using Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

# to run the container:
# docker build -t genai-recommendations .
# docker run -d -p 8000:8000 genai-recommendations
# http://localhost:8000/recommendations/M001?output=json