# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app directory contents to workdir
COPY app/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8888

# Command to run the application
CMD ["python", "chat.py"]