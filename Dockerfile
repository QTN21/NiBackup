# Use an official Python image as a base
FROM python:3.9-slim

# Set the environment variable for the password
ENV PASS=pass
# Set the environment variable
ENV PYTHONUNBUFFERED=1

# Set the working directory to /app
WORKDIR /app

# Install 
RUN apt update && apt install -y libsqlcipher-dev git python3-pip

# Download the repository from GitHub
RUN git clone https://github.com/QTN21/NIBackup.git .

# Install the dependencies
RUN pip3 install -r ./requirements.txt

# Run the command when the container starts
CMD python3 script.py "$PASS"