from fastapi import FastAPI, Request
import logging

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        print(f"Received webhook data: {data}")
        logging.info(f"Received webhook data: {data}")
        return {"status": "ok", "received": data}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
