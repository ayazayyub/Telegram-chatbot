# Dockerfile
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    ffmpeg \
    git \
    gcc \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Configure Python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

# Application setup
WORKDIR /app
COPY . .

# Environment variables
ENV TELEGRAM_TOKEN=your_bot_token
ENV HF_HOME=/app/cache/huggingface
ENV HF_DATASETS_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1

# Volumes for cache and models
VOLUME /app/cache
VOLUME /app/models

# Run the bot
CMD ["python", "-m", "__main__.py"]
