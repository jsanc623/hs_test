import requests

from url import builder


def post(dataset):
    url = builder("result")
    return requests.post(url, json=dataset, headers={
        'Content-type': 'application/json',
        'Accept': 'application/json'
    })


def get():
    return requests.get(builder())
