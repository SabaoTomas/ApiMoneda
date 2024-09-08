# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
# If there are no dependencies, this line can be omitted
RUN pip install flask
RUN pip install flask-cors

# Make port 8080 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the simple Python HTTP server
CMD ["python", "-m", "http.server", "8080"]
