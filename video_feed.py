from aiohttp import web
import time
import cv2
import base64

vid = None
fps = None
quality = None

def init(config):
    global vid
    global fps
    global quality

    vid = cv2.VideoCapture(config['video']['camera_index'])
    fps = config['video']['fps']
    quality = config['video']['quality']

last_frame_base64_str = ""
last_frame_capture_date = 0
def get_video_frame() -> str:
    global last_frame_capture_date
    global last_frame_base64_str

    # if frame has already been captured within FPS, send latest cached frame
    if time.time() - last_frame_capture_date < (1 / fps):
        return last_frame_base64_str
    
    ret, frame = vid.read()
    ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
    encoded_frame = base64.b64encode(buffer)
    last_frame_base64_str = encoded_frame.decode('utf-8')
    last_frame_capture_date = time.time()
    return last_frame_base64_str

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        frame = get_video_frame()
        await ws.send_str(frame)
        time.sleep(1 / fps)