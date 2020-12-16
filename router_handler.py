from aiohttp.web import json_response
import pandas as pd

import logging
from datetime import datetime
from json.decoder import JSONDecodeError

from utils.errors import ApiBadRequest
from recommend import Recommender
from prepare_data import prepare_data, split_train_test
from config import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')


class RouterHandler(object):
    def __init__(self, loop):
        self._loop = loop
        self.path = BX_path
        self.recommender = Recommender(BX_similarities)

    async def train(self, request):
        start = datetime.now()
        self.recommender.train()
        end = datetime.now()
        return json_response({
            "status": "Success",
            "time": str(end - start)
        })

    async def evaluation(self, request):
        body = await decode_request(request)
        able_fields = ['metric', 'loss']
        body = filter_fields(able_fields, body)

        try:
            test_set = pd.read_csv(os.path.join(self.path, 'test.csv'), sep=';', dtype=object).to_numpy().tolist()
        except Exception as err:
            logging.exception(err)
            return json_response({
                "status": "Fail",
                "detail": "Data is not correct"
            })

        start = datetime.now()
        mae, rmse, predicted_ratio = self.recommender.get_mae(test_set)
        results = {
            "status": "Success",
            "MAE": mae,
            "RMSE": rmse,
            "predicted_ratio": predicted_ratio
        }

        if body.get('loss'):
            loss = self.recommender.get_score(test_set, mode=body.get('loss'))
            if type(loss) == tuple:
                loss = {
                    "f1_score": loss[0],
                    "rankscore": loss[1],
                    "avg_precision": loss[2]
                }
            results['loss'] = loss
        end = datetime.now()
        time = end - start

        results['time'] = time.total_seconds()

        return json_response(results)

    async def prediction(self, request):
        body = await decode_request(request)
        required_fields = ['user']
        validate_fields(required_fields, body)

        user = str(body.get('user'))

        start = datetime.now()
        predicted = self.recommender.prediction(user)
        end = datetime.now()
        time = end - start

        if predicted:
            return json_response({
                "status": "Fail",
                "detail": "Image not found"
            })

        return json_response({
            "status": "Success",
            "recommend": [book for book, _ in predicted],
            "time": time.total_seconds()
        })

    async def prepare(self, request):
        try:
            ratings = pd.read_csv(os.path.join(self.path, 'ratings.csv'), sep=';')
            split_train_test(ratings, self.path)

            train_path = os.path.join(self.path, 'train.csv')
            prepare_data(train_path)

            return json_response({
                "status": 'Success'
            })
        except Exception as err:
            logging.exception(err)
            return json_response({
                "status": "Fail"
            })

    async def predict_rate(self, request):
        body = await decode_request(request)
        required_fields = ['user', 'book']
        validate_fields(required_fields, body)

        user = str(body.get('user'))
        book = str(body.get('book'))

        start = datetime.now()
        rate = self.recommender.predict_rate(user, book)
        end = datetime.now()
        time = end - start

        if rate:
            return json_response({
                "status": "Fail",
                "detail": "Image not found",
                "time": time.total_seconds()
            })

        return json_response({
            "status": "Success",
            "predicted": rate,
            "time": time.total_seconds()
        })


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest('Improper JSON format')


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest("'{}' parameter is required".format(field))


def filter_fields(able_fields, body):
    result = {}
    for field in able_fields:
        if body.get(field):
            result[field] = body.get(field)
    return result
