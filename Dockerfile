# Use an official Python image as a base
FROM python:3.9-slim

# Set the environment variable for the password
ENV PASSWORD=my_secret_password

# Set the environment variable
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Install 
RUN apt-get update && apt-get install libsqlcipher-dev

# Download the repository from GitHub
RUN git clone https://github.com/NIP_Backup .

# Install the dependencies
RUN pip install --no-cache-dir -r ./NIP_Backup/requirements.txt

# Run the command when the container starts
CMD ["python3", "script.py", "${PASSWORD}"]

# Share the backup.csv file between the Docker container and the system
VOLUME ./backup.csv:/app/NIP_Backup/files/backup.csv