# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required by OpenCV and other image processing libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Start gunicorn with app:app, where the left `app` is the module name (app.py) and the right `app` is the Flask application instance within that module
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
