import cv2
import base64
import asyncio
from websockets.server import serve
import time

FPS = 10
COMPRESSION_PERCENTAGE = 20

vid = cv2.VideoCapture(2)

last_frame_base64_str = ""
last_frame_capture_date = 0
def get_video_frame() -> str:
    global last_frame_capture_date
    global last_frame_base64_str


    # if frame has already been captured within FPS, send latest cached frame
    if time.time() - last_frame_capture_date < (1 / FPS):
        return last_frame_base64_str
    
    ret, frame = vid.read()
    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, COMPRESSION_PERCENTAGE])
    encoded_frame = base64.b64encode(buffer)
    last_frame_base64_str = encoded_frame.decode('utf-8')
    last_frame_capture_date = time.time()
    return last_frame_base64_str


async def echo(websocket):
    print(" Punk Detetcted...")
    while True:
        frame = get_video_frame()
        await websocket.send(str(frame))
        await asyncio.sleep(1 / FPS)

async def main():
    async with serve(echo, "localhost", 6969):
        await asyncio.Future()  # run forever
       

asyncio.run(main())