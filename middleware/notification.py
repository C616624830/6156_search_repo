import requests
import json
import middleware.context as context
import boto3


class NotificationMiddlewareHandler:
    def __init__(self):
        pass

    @staticmethod
    def notify(request, response):
        subscriptions = context.get_context("SUBSCRIPTIONS")
        notification = {}
        if request.path in subscriptions:
            try:
                request_data = request.get_json()
            except Exception as e:
                request_data = None
            path = request.path

            if request.method == 'POST':
                notification["change"] = "CREATED"
                notification["new_state"] = request_data
                notification["params"] = path
            elif request.method == 'PUT':
                notification["change"] = "UPDATE"
                notification["new_state"] = request_data
                notification["params"] = path
            elif request.method == 'DELETE':
                notification["change"] = "DELETE"
                notification["new_state"] = request_data
                notification["params"] = path
            else:
                notification = None
            if notification.get("change", None):
                request_data = json.dumps(notification)
                request_data = json.dumps({'text': request_data})
                # response = requests.post(
                #     NotificationMiddlewareHandler.slack_url, data=request_data,
                #     headers={'Content-Type': 'application/json'}
                # )
                # print("Response = ", response.status_code)
                client = boto3.client('sns', region_name='us-east-2',
                                      aws_access_key_id='AKIA6NSFGNTPRI6FWF73',
                                      aws_secret_access_key= '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')
                client.publish(TopicArn="arn:aws:sns:us-east-2:991208828127:SNS_user_changed",
                               Message=request_data)
