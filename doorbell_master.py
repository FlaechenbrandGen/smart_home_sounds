'''
This script is a FastAPI application that starts ringing a doorbells by sending GET requests to specified URLs.
It uses asynchronous HTTP requests to ensure that the doorbell ringing process is non-blocking.
It is designed to be run as a service, and it will attempt to ring the doorbell at each URL in the list up to 10 times.
'''
from time import sleep
from fastapi import FastAPI
import httpx
import asyncio
import logging

app = FastAPI()
URLS= [
    "http://klingel-arbeitszimmer:8000",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ring_doorbell(url)->None:
    async with httpx.AsyncClient() as client:
        for i in range(10):
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    break
            except Exception as e:
                logger.error(f"Error while ringing doorbell at {url}: {e}")
                sleep(1)

async def send_audio_file(url: str, file_path: str) -> None:
    """Send audio file via POST to the specified URL"""
    async with httpx.AsyncClient() as client:
        try:
            with open(file_path, 'rb') as audio_file:
                files = {'file': audio_file}
                response = await client.post(url, files=files)
                if response.status_code == 200:
                    logger.info(f"Audio file sent successfully to {url}")
                else:
                    logger.error(f"Failed to send audio file to {url}: {response.status_code}")
        except Exception as e:
            logger.error(f"Error while sending audio file to {url}: {e}")




@app.get("/doorbell")
async def doorbell():
    for url in URLS:
        myurl = url+ "/doorbell"
        asyncio.create_task(ring_doorbell(myurl))  # Run the task without waiting for completion
    return

@app.get("/alarm")
async def doorbell():
    for url in URLS:
        myurl = url+ "/alarm"
        asyncio.create_task(ring_doorbell(myurl))  # Run the task without waiting for completion
    return

@app.get("/waschmaschine_fertig")
async def waschmaschine_fertig():
    for url in URLS:
        play_url = url + "/play"
        file_path = "WaschmaschineFertig_German_Vicki.mp3"
        asyncio.create_task(send_audio_file(play_url, file_path))
    return {"message": "Audio file transmission started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)