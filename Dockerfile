# syntax=docker/dockerfile:1

# Use the official Python 3.10.9 image as a base image
FROM python:3.10.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy everything from the current directory to /app in the container
COPY . /app

# Install any dependencies in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Inform Docker that the container is listening on port 3100 at runtime.
EXPOSE 3100

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "3100"]
