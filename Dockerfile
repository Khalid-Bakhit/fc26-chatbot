# Use official Python base image
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code, templates, static, and data
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY data/ /app/data/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Default command: use gunicorn to serve the Flask app
CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:5000"]
