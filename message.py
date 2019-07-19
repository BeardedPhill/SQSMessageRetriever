import time

class Message():
    def __init__(self, message=None):
        timestamp = float(message['Attributes']['SentTimestamp']) / 1000
        self.id = message['MessageId']
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        self.body = message['Body']
