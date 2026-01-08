FROM python:3.13-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Install system dependencies (Required for PostgreSQL and other libs)
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy project files
COPY . .

# Change ownership to the non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Run collectstatic so WhiteNoise can serve files
RUN python manage.py collectstatic --noinput

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start the server using Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
