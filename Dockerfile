# Use a lightweight base image
FROM python:3.8-alpine

LABEL authors="Fred Assi"
LABEL maintainer="assifred2005@gmail.com"

# Set the working directory
WORKDIR /app

# Copy application files
COPY rest_app.py config.py db_connector.py requirements.txt /app/

# Install curl and system dependencies
RUN apk --no-cache add curl && \
    apk update && \
    apk upgrade && \
    apk --no-cache add build-base libffi-dev openssl-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application will run on
EXPOSE 5003

# Create a volume for logs
VOLUME /app/logs

# Specify the user to run the application
USER myuser

# Health check command (optional)
HEALTHCHECK CMD curl -f http://localhost:5003/users/1 || exit 1

# Command to run the application
CMD ["python3", "rest_app.py"]