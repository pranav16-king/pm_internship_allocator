# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run your app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
