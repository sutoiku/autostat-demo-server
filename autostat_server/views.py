from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from autostat.kernel_search import find_best_kernel_and_predict
from autostat.kernel_tree_types import NpDataSet
from autostat.kernel_trees_sklearn import SklearnGPModel

import numpy as np

import json

# Create your views here.


def reshape(v):
    return np.array(v).reshape(-1, 1)


@csrf_exempt
def index(request):
    data_str = request.body
    try:
        data = json.loads(data_str)
    except Exception as e:
        print(repr(e))
        str_resp = "JSON DID NOT PARSE -- " + repr(e) + "\n\n" + repr(data_str)
        data = None

    try:
        dataset = NpDataSet(
            *[reshape(data[k]) for k in ["train_x", "train_y", "test_x", "test_y"]]
        )
    except Exception as e:
        print(repr(e))
        str_resp = "DATASET OBJECT NOT CREATED -- " + repr(e) + "\n\n" + repr(data_str)
        dataset = None

    try:
        y, lower, upper = find_best_kernel_and_predict(
            dataset, SklearnGPModel, search_iterations=2
        )
        str_resp = json.dumps(
            {"mean": list(y), "lower": list(lower), "upper": list(upper)}
        )
    except Exception as e:
        print(repr(e))
        str_resp = "FIT+PREDICT FAILED -- " + repr(e) + "\n\n" + repr(data_str)

    return HttpResponse(f"Hello from Python~~!\n{str_resp}\n\n")
