from time import sleep
from fastapi import FastAPI
import httpx

app = FastAPI()
URLS= [
    "http:/klingel-arbeitszimmer:8000/doorbell",
]

async def ring_doorbell(url)->None:
    async with httpx.AsyncClient() as client:
        for i in range(10):
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    print(f"Doorbell sound played successfully at {url}")
                    break
            except Exception as e:
                sleep(1)



@app.get("/doorbell")
async def doorbell():
    for url in URLS:
        ring_doorbell(url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)