from aiohttp import web

from settings import config
import video_feed

async def index(request):
    raise web.HTTPFound('/client/index.html')

def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_get("/video", video_feed.websocket_handler)
    app.router.add_static('/client', "client")

video_feed.init(config)

app = web.Application()
setup_routes(app)
app['config'] = config

web.run_app(app, host=config['server']['host'], port=config['server']['port'])