# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY backend/ /app

# Expose the port your application runs on
EXPOSE 5000  # Adjust based on your Flask or Dash app port

# Command to run the application (e.g., Flask or Dash)
CMD ["python", "app.py"]