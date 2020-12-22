import logging
import sys
import asyncio
import argparse

from aiohttp import web
from zmq.asyncio import ZMQEventLoop

from router_handler import RouterHandler
from config import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='Recommendation System')

    parser.add_argument(
        '-d', '--data',
        help='Dataset to run system',
        default='BX'
    )

    return parser.parse_args()


def start_server(host, port):
    args = parse_args()
    _loop = asyncio.get_event_loop()
    app = web.Application(loop=_loop, client_max_size=20*1024**2)

    # data_path = data_paths[args.data]
    handler = RouterHandler(_loop, args.data)

    app.router.add_get('/train', handler.train)
    app.router.add_post('/evaluate', handler.evaluate)
    app.router.add_get('/eval_error', handler.evaluate_error)
    app.router.add_post('/recommend', handler.recommend)
    app.router.add_post('/predict', handler.predict)
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
