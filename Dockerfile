# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir pandas

# Expose port 80 to allow communication to/from server
EXPOSE 80

# Define environment variables
ENV TEAM1_FILE="team1.csv" \
    TEAM2_FILE="team2.csv"

# Command to run the application
CMD ["python", "sim-csv.py"]
