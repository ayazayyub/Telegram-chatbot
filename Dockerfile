# Use official CUDA base image
FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Environment configuration
ENV PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/cache/huggingface

# Security best practice for Telegram token (DO NOT hardcode here!)
ARG TELEGRAM_TOKEN
ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}

# Create cache directory and set permissions
RUN mkdir -p ${HF_HOME} && chmod 777 ${HF_HOME}

# Persistent storage for Hugging Face models
VOLUME /app/cache

# Install PyTorch with CUDA 12.1 first
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    torchaudio==2.1.0 \
    --extra-index-url https://download.pytorch.org/whl/cu121

# Copy and install other requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "telegram_chatbot"]
