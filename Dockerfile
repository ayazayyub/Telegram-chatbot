# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV TELEGRAM_TOKEN=your_telegram_token
ENV OPENAI_API_KEY=your_openai_key
ENV UNSPLASH_API_KEY=optional_unsplash_key

# Run the bot
CMD ["python", "__main__.py"]
