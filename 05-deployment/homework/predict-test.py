#!/usr/bin/env python

import requests


url = 'http://localhost:9696/predict'

clients = {}

clients['client_Q3'] = {
    "job": "retired",
    "duration": 445,
    "poutcome": "success"
}

clients['client_Q4'] = {
    "job": "unknown",
    "duration": 270,
    "poutcome": "failure"
}

for client_id, client in clients.items():
    response = requests.post(url, json=client).json()
    print(f'{client_id}: {client}')
    print(response)

    if response['get_credit'] == True:
        print('Client will get credit.')
    else:
        print('Client will not get credit.')

    print()
