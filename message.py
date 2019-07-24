import time
import json

class Message():
    def __init__(self, message=None):
        timestamp = float(message['Attributes']['SentTimestamp']) / 1000
        message_body = json.loads(message['Body'])

        self.id = message['MessageId']
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        try:
            if message_body['Type']=='Notification':
                self.body = message_body['Message']
            else:
                self.body = json.dumps(message_body)
        except KeyError:
            self.body = json.dumps(message_body)


class SqsFormData():
    def __init__(self, queue_url=None, max_messages=None, delete_messages=None):
        self.queue_url = queue_url
        self.max_messages = max_messages
        self.delete_messages = delete_messages
