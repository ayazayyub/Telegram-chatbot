FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# System dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

# Application setup
WORKDIR /app
ENV PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1
COPY . .

# Environment variables
ENV TELEGRAM_TOKEN=your_bot_token
ENV HF_HOME=/app/cache/huggingface
ENV HF_DATASETS_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1


# Run the bot
CMD ["python", "-m", "telegram_chatbot"]
