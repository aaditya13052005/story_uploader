# utils/asr_deepgram.py

import logging
import aiohttp
import asyncio
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="asr_deepgram.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DEEPGRAM_API_KEY = Config.DEEPGRAM_API_KEY
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen?punctuate=true&word_offsets=true"


# ------------------------- Core Function -------------------------
async def transcribe_audio(file_path: str):
    """
    Transcribe audio using Deepgram API and return list of words with timestamps.
    :param file_path: Path to the audio file.
    :return: List of dicts [{word, start, end}, ...]
    """
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as audio_file:
                async with session.post(
                    DEEPGRAM_URL,
                    headers=headers,
                    data=audio_file
                ) as response:
                    if response.status != 200:
                        logging.error(f"Deepgram API error: {response.status}")
                        return []

                    result = await response.json()
                    words = []

                    # Navigate Deepgram JSON safely
                    items = (
                        result.get("results", {})
                              .get("channels", [{}])[0]
                              .get("alternatives", [{}])[0]
                              .get("words", [])
                    )

                    for w in items:
                        words.append({
                            "word": w.get("word", ""),
                            "start": float(w.get("start", 0.0)),
                            "end": float(w.get("end", 0.0))
                        })

                    return words

    except Exception as e:
        logging.error(f"Exception in transcribe_audio: {e}")
        return []


# ------------------------- Sync Wrapper -------------------------
def transcribe_audio_sync(file_path: str):
    """
    Synchronous wrapper for Flask routes or scripts.
    """
    return asyncio.run(transcribe_audio(file_path))
