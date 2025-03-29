# Use an official Python runtime as a parent image
FROM python:3.13-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use a smaller base image for the final build
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the current directory contents into the container at /app
COPY . .

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser

# Make port 4999 available to the world outside this container
EXPOSE 4999

# Define environment variable
ENV FLASK_APP=main.py

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:4999", "main:app"]