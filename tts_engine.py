import uuid
import os
import logging
from werkzeug.utils import secure_filename
from config import Config
from gtts import gTTS

# Setup
OUTPUT_DIR = Config.UPLOAD_FOLDER
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO, filename="audio_generation.log")

# Default language
DEFAULT_LANG = "en"

def gtts_generate(text, lang=DEFAULT_LANG):
    try:
        # Generate a unique file name
        file_name = secure_filename(f"{uuid.uuid4()}.mp3")
        output_path = os.path.join(OUTPUT_DIR, file_name)

        # Create TTS audio and save
        tts = gTTS(text=text, lang=lang)
        tts.save(output_path)

        logging.info(f"✅ GTTS audio saved: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"[ERROR] GTTS failed: {e}")
        return None

def generate_tts(text, lang=DEFAULT_LANG):
    return gtts_generate(text, lang)
