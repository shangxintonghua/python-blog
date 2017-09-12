import logging; logging.basicConfig(level=logging.INFO)
import asyncio,os,json,time
from datetime import datetime
from www.coreweb import add_routes,add_static

from aiohttp import web
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')

@asyncio.coroutine
def logger_factory(app,handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request:%s%s'%(request.method,
                                     request.path))
        return (yield from handler(request))
    return logger

@asyncio.coroutine
def response_factory(app,handler):
    @asyncio.coroutine
    def response(request):
        r=yield from handler(request)
        if isinstance(r,web.StreamResponse):
            return  r
        if isinstance(r,bytes):
            resp=web.Response(body=r)
            resp.content_type='application/octet-stream'
            return resp
        if isinstance(r,str):
            resp=web.Response(body=r.encode('utf-8'))
            resp.content_type='text/html;charset=utf-8'
            return resp

@asyncio.coroutine
def init(loop):
    app=web.Application(loop=loop,middlewares=[logger_factory,
                                               response_factory])
    init_jinja2(app,filter=dict(datetime=datetime_filter))
    add_routes(app,'handlers')
    add_static(app)


    srv=yield from loop.create_server(app.make_handler(),'127.0.0.1',9000)
    logging.info('server started at http://127.0.0.1:9000')
    return srv
loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()