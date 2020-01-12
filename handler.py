# import json


# def hello(event, context):
#     body = {
#         "message": "Go Serverless v1.0! Your function executed successfully!",
#         "input": event
#     }

#     response = {
#         "statusCode": 200,
#         "body": json.dumps(body)
#     }

#     return response

#     # Use this code if you don't use the http event with the LAMBDA-PROXY
#     # integration
#     """
#     return {
#         "message": "Go Serverless v1.0! Your function executed successfully!",
#         "event": event
#     }
#     """

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import telegram

TOKEN = os.environ['TELEGRAM_TOKEN']
TARGET_USER_ID = int(os.environ['TARGET_USER_ID'])
BOT = telegram.Bot(token=TOKEN)

RES = {"statusCode": 200}

KEYWORDS = [
    'stayman',
    'meeting',
    'announcement',
    'important',
    'conference',
    'gather',
    'registration',
    'retreat',
    'urgent',
    'schedule'
]

def forward(data):
    BOT.forwardMessage(TARGET_USER_ID, data['message']['chat']['id'], data['message']['message_id'])

def telegram_web_hook(event, context):
    try:
        data = json.loads(event["body"])
        if TARGET_USER_ID == data['message']['from']['id']:
            return RES
        if 'text' not in data['message']:
            return RES
        text = data['message']['text'].lower()
        for keyword in KEYWORDS:
            if keyword in text:
                forward(data)
                return RES
        
    except Exception as e:
        print(e)

    return RES
