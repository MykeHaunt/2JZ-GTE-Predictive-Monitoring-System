# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy environment
COPY environment.yml /app/
RUN pip install --upgrade pip && pip install pipenv && pipenv install --system --deploy

# Copy project files
COPY backend/ /app/backend/
COPY model.pkl /app/
COPY logs/ /app/logs/

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "backend/app.py"]