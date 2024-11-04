# Use the official Python image as a base image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /authentication_service

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/authentication_service/src

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory into the container
COPY src/ ./src/

# Expose port 8000 for the FastAPI application
EXPOSE 8000

ENTRYPOINT [ "python", "src/app.py" ]