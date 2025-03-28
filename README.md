# AI-Powered Telegram Bot 🤖✨

A feature-rich Telegram bot leveraging OpenAI's API to provide:
- 🖼️ **Text-to-ImageGeneration** (DALL-E 3)
- 💬 **Smart Q&A** (GPT-4)
- 🎥 **Simple Video Creation** (Image sequences)

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Bot Demo](https://via.placeholder.com/800x400.png?text=Sample+Bot+Interface) <!-- Replace with actual screenshots -->

## Features 🚀

| Command                  | Description                          | Example                     |
|--------------------------|--------------------------------------|-----------------------------|
| `/start`                 | Show welcome message                 |                             |
| `/image <prompt>`        | Generate AI artwork                  | `/image cyberpunk cat`      |
| `/ask <question>`        | Get expert answers                   | `/ask Explain quantum physics simply` |
| `/video <prompt>`        | Create 5-second video                | `/video sunset over mountains` |

## Installation 📦

### Prerequisites
- Python 3.11+
- Docker (optional)
- [Telegram Bot Token](https://core.telegram.org/bots#6-botfather)
- [OpenAI API Key](https://platform.openai.com/api-keys)

### Local Setup
```bash
git clone https://github.com/ayazayyub/telegram-chatbot.git
cd telegram-chatbot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_TOKEN="your_bot_token"
export OPENAI_API_KEY="your_openai_key"

# Run the bot
python __main__.py
