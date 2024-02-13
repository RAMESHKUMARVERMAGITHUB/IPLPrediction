# Use an official Python runtime as a base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pandas
RUN pip install --no-cache-dir pandas

# Expose ports for Flask
EXPOSE 5000

# Run the Python script
CMD ["python", "app.py"]
