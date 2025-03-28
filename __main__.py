# __main__.py
import os
import logging
import tempfile
import requests
import torch
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from moviepy.editor import ImageSequenceClip

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MODEL_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize AI models
text_pipeline = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.1",
    device=MODEL_DEVICE,
    torch_dtype=torch.float16 if MODEL_DEVICE == "cuda" else torch.float32
)

image_pipeline = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16 if MODEL_DEVICE == "cuda" else torch.float32
).to(MODEL_DEVICE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    await update.message.reply_text(
        "🤖 Free AI Bot\n"
        "/ask <question> - Get answers\n"
        "/image <prompt> - Generate images\n"
        "/video <prompt> - Create short videos"
    )

async def generate_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text generation requests"""
    try:
        prompt = ' '.join(context.args)
        if not prompt:
            await update.message.reply_text("Please enter a question after /ask")
            return

        async with update.message.chat.send_action(action="typing"):
            response = text_pipeline(
                prompt,
                max_length=200,
                do_sample=True,
                temperature=0.7
            )
            
        await update.message.reply_text(response[0]['generated_text'])
        
    except Exception as e:
        logger.error(f"Text generation error: {str(e)}")
        await update.message.reply_text("Error generating response")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image generation requests"""
    try:
        prompt = ' '.join(context.args)
        if not prompt:
            await update.message.reply_text("Please enter a prompt after /image")
            return

        async with update.message.chat.send_action(action="upload_photo"):
            image = image_pipeline(prompt).images[0]
            
            # Save temporary image
            with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
                image.save(temp_file.name)
                await update.message.reply_photo(photo=open(temp_file.name, 'rb'))
                
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        await update.message.reply_text("Error generating image")

async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video generation requests"""
    try:
        prompt = ' '.join(context.args)
        if not prompt:
            await update.message.reply_text("Please enter a prompt after /video")
            return

        async with update.message.chat.send_action(action="upload_video"):
            # Generate 3 frames
            frames = []
            for i in range(3):
                result = image_pipeline(f"{prompt} - frame {i+1}")
                frames.append(result.images[0])
            
            # Create video
            with tempfile.TemporaryDirectory() as tmp_dir:
                frame_paths = []
                for idx, frame in enumerate(frames):
                    path = f"{tmp_dir}/frame_{idx}.png"
                    frame.save(path)
                    frame_paths.append(path)
                
                clip = ImageSequenceClip(frame_paths, fps=2)
                video_path = f"{tmp_dir}/output.mp4"
                clip.write_videofile(video_path, codec="libx264", logger=None)
                
                await update.message.reply_video(
                    video=InputFile(video_path),
                    caption="Generated video"
                )
                
    except Exception as e:
        logger.error(f"Video generation error: {str(e)}")
        await update.message.reply_text("Error generating video")

def main():
    """Run the bot"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ask", generate_answer))
    application.add_handler(CommandHandler("image", generate_image))
    application.add_handler(CommandHandler("video", generate_video))
    
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
