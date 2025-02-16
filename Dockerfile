# Use Python 3.9 slim as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the application code into the container
COPY . /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Define environment variable
ENV NAME World

# Set the command to run the Flask application
CMD ["python", "app.py"]
