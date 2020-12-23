from aiohttp.web import json_response
import pandas as pd

import logging
from datetime import datetime
from json.decoder import JSONDecodeError

from utils.errors import ApiBadRequest
from recommend import Recommender
from config import *

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

data_paths = {'BX': [BX_path, 10], 'GB': [GB_path, 5]}


class RouterHandler(object):
    def __init__(self, loop, data):
        self._loop = loop
        self.path = data_paths[data][0]
        self.rate_max = data_paths[data][1]
        similarities_path = os.path.join(self.path, 'data_matrix_similarities')
        dataset = 1 if data == 'BX' else 2
        self.recommender = Recommender(similarities_path, rate_max=self.rate_max, dataset=dataset)

    async def train(self, request):
        start = datetime.now()
        self.recommender.train()
        end = datetime.now()
        return json_response({
            "status": "Success",
            "time": str(end - start)
        })

    async def evaluate(self, request):
        body = await decode_request(request)
        able_fields = ['n_samples']
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
        n_samples = 20
        if body.get('n_samples'):
            n_samples = int(body.get('n_samples'))

        scores = self.recommender.evaluation(test_set, n_samples=n_samples)
        end = datetime.now()
        time = end - start

        results = {
            "precision": scores[0],
            "recall": scores[1],
            "f1_score": scores[2],
            "rankscore": scores[3],
            "time": time.total_seconds()
        }

        return json_response(results)

    async def evaluate_error(self, request):
        try:
            test_set = pd.read_csv(os.path.join(self.path, 'test.csv'), sep=';', dtype=object).to_numpy().tolist()
        except Exception as err:
            logging.exception(err)
            return json_response({
                "status": "Fail",
                "detail": "Data is not correct"
            })

        start = datetime.now()
        mae, rmse, predicted_ratio = self.recommender.get_error(test_set)
        end = datetime.now()
        time = end - start

        results = {
            "status": "Success",
            "MAE": mae,
            "RMSE": rmse,
            "predicted_ratio": predicted_ratio,
            "time": time.total_seconds()
        }

        return json_response(results)


    async def recommend(self, request):
        body = await decode_request(request)
        required_fields = ['user']
        validate_fields(required_fields, body)

        user = str(body.get('user'))

        start = datetime.now()
        predicted = self.recommender.prediction(user, n_pred=10)
        end = datetime.now()
        time = end - start

        print(predicted, '\n')

        if not predicted:
            return json_response({
                "status": "Fail",
                "detail": "User is cold start",
                "time": time.total_seconds()
            })

        return json_response({
            "status": "Success",
            "recommend": [book for book, _ in predicted],
            "time": time.total_seconds()
        })

    async def predict(self, request):
        body = await decode_request(request)
        required_fields = ['user', 'book']
        validate_fields(required_fields, body)

        user = str(body.get('user'))
        book = str(body.get('book'))

        start = datetime.now()
        rate = self.recommender.predict_rate(user, book)
        end = datetime.now()
        time = end - start

        print("Rate: ", rate)

        if not rate:
            return json_response({
                "status": "Fail",
                "detail": "Can't predict",
                "time": time.total_seconds()
            })

        return json_response({
            "status": "Success",
            "predicted": rate,
            "time": time.total_seconds()
        })

    # async def prepare(self, request):
    #     try:
    #         # ratings = pd.read_csv(os.path.join(self.path, 'ratings.csv'), sep=';')
    #         # split_train_test(ratings, self.path)
    #
    #         train_path = os.path.join(self.path, 'train.csv')
    #         prepare_data(train_path)
    #
    #         return json_response({
    #             "status": 'Success'
    #         })
    #     except Exception as err:
    #         logging.exception(err)
    #         return json_response({
    #             "status": "Fail"
    #         })


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
