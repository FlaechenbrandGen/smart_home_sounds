import os
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "plughw:1,0"
# os.environ["SDL_AUDIO_DEVICE"] = "plughw:1,0"
from fastapi import FastAPI, Request
import pygame
import logging
import io
import tempfile
import threading
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


app = FastAPI()
#pygame.mixer.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

@app.get("/doorbell")
def doorbell():
    try:
        # Pfad zur Audiodatei
        audio_file = "/home/gerhard/doorbell/G5_05.wav"
        
        # Prüfen ob Datei existiert
        if not os.path.exists(audio_file):
            return {"error": f"Audio file {audio_file} not found"}
        
        # Audiodatei laden und abspielen
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        return {"message": "Doorbell sound played!"}
    
    except Exception as e:
        return {"error": f"Failed to play sound: {str(e)}"}


@app.get("/alarm")
def doorbell():
    try:
        # Pfad zur Audiodatei
        audio_file = "/home/gerhard/doorbell/tng_red_alert2.mp3"
        
        # Prüfen ob Datei existiert
        if not os.path.exists(audio_file):
            return {"error": f"Audio file {audio_file} not found"}
        
        # Audiodatei laden und abspielen
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        return {"message": "Doorbell sound played!"}
    
    except Exception as e:
        return {"error": f"Failed to play sound: {str(e)}"}
    
@app.post("/play")
async def play(request: Request):
    ''' Play a sound from bytestring from a post request '''
    try:
        # Read the raw bytes from the request body
        audio_bytes = await request.body()
        
        if not audio_bytes:
            return {"error": "No audio data received"}
        
        logger.info(f"Received audio data: {len(audio_bytes)} bytes")

        # pygame.mixer.music.load(buffer=audio_bytes)
        # pygame.mixer.music.play()
        
        #Create a temporary file to store the audio data
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Load and play using pygame.mixer.music (same as working endpoints)
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()
            
            logger.info(f"Audio file loaded and playing: {temp_file_path}")
            
            return {"message": "Audio played successfully!"}
        
        finally:
            # Clean up the temporary file after a short delay
            def cleanup():
                time.sleep(10)  # Wait a bit before cleanup
                try:
                    os.unlink(temp_file_path)
                    logger.info(f"Temporary file cleaned up: {temp_file_path}")
                except:
                    pass
            threading.Thread(target=cleanup, daemon=True).start()
    
    except Exception as e:
        logger.error(f"Failed to play audio: {str(e)}")
        return {"error": f"Failed to play sound: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
