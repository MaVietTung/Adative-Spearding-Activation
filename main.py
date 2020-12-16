import logging
import sys
import asyncio
from aiohttp import web
from zmq.asyncio import ZMQEventLoop
from router_handler import RouterHandler

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def start_server(host, port):
    _loop = asyncio.get_event_loop()
    app = web.Application(loop=_loop, client_max_size=20*1024**2)

    app['aes_key'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    app['private_key'] = '0xab0880a6a9b593b6b4dfb23b842716f5777ff8656df940f137b00cc3ed76be2d'

    handler = RouterHandler(_loop)

    app.router.add_get('/train', handler.train)
    app.router.add_post('/evaluation', handler.evaluation)
    app.router.add_post('/prediction', handler.prediction)
    app.router.add_post('/predict', handler.predict_rate)
    app.router.add_get('/prepare', handler.prepare)

    LOGGER.info('Starting Server on %s:%s', host, port)
    web.run_app(
        app,
        host=host,
        port=port,
        access_log=LOGGER,
        access_log_format='%r: %s status, %b size, in %Tf s'
    )


def main():
    loop = ZMQEventLoop()
    asyncio.set_event_loop(loop=loop)

    try:
        start_server('localhost', 8096)
    except Exception as err:
        LOGGER.exception(err)
        sys.exit(1)


if __name__ == '__main__':
    main()
