import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import requests
import tempfile
from moviepy.editor import ImageSequenceClip

# Configure API Keys
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")  # Optional for real images

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! I can:\n"
        "- Generate images from text prompts (/image <prompt>)\n"
        "- Answer questions (/ask <question>)\n"
        "- Create videos from text (/video <prompt>)"
    )

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Please provide a prompt after /image")
        return

    try:
        # Generate image using DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        await update.message.reply_photo(image_url)
        
    except Exception as e:
        await update.message.reply_text(f"Error generating image: {str(e)}")

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = ' '.join(context.args)
    if not question:
        await update.message.reply_text("Please provide a question after /ask")
        return

    try:
        # Generate answer using GPT-4
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        
        answer = response.choices[0].message.content
        await update.message.reply_text(answer)
        
    except Exception as e:
        await update.message.reply_text(f"Error generating answer: {str(e)}")

async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = ' '.join(context.args)
    if not prompt:
        await update.message.reply_text("Please provide a prompt after /video")
        return

    try:
        # Generate multiple images for video
        images = []
        for _ in range(5):  # Generate 5 frames
            response = client.images.generate(
                model="dall-e-3",
                prompt=f"{prompt} - frame {_+1}/5",
                size="512x512",
                n=1,
            )
            images.append(requests.get(response.data[0].url).content)

        # Create video from images
        with tempfile.TemporaryDirectory() as tmp_dir:
            frame_paths = []
            for i, img_data in enumerate(images):
                path = f"{tmp_dir}/frame_{i}.png"
                with open(path, "wb") as f:
                    f.write(img_data)
                frame_paths.append(path)

            clip = ImageSequenceClip(frame_paths, fps=1)
            video_path = f"{tmp_dir}/output.mp4"
            clip.write_videofile(video_path, codec="libx264")

            await update.message.reply_video(InputFile(video_path))
            
    except Exception as e:
        await update.message.reply_text(f"Error generating video: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("image", generate_image))
    application.add_handler(CommandHandler("ask", answer_question))
    application.add_handler(CommandHandler("video", generate_video))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
