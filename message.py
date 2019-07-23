import time

class Message():
    def __init__(self, message=None):
        timestamp = float(message['Attributes']['SentTimestamp']) / 1000
        self.id = message['MessageId']
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        self.body = message['Body']

class SqsFormData():
    def __init__(self, queue_url=None, max_messages=None, delete_messages=None):
        self.queue_url = queue_url
        self.max_messages = max_messages
        self.delete_messages = delete_messages
