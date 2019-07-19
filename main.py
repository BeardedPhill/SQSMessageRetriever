from flask import Flask, escape, request, render_template
from message import Message
import sys
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('get_messages_form.html')

@app.route("/get_sqs_messages", methods=["POST"])
def get_messages():
    for key, value in request.form.items():
        if (key=="SQS_URL"):
            queue_url = value

    messages = call_sqs(queue_url)
    return render_template('index.html', messages=messages)

def get_messages_from_queue(queue_url):
    sqs_client = boto3.client('sqs')

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

        try:
            for message in resp['Messages']:
                yield message
        except KeyError:
            return

def call_sqs(queue_url):
    messages=[]
    for message in get_messages_from_queue(queue_url):
        messages.append(Message(message))

    return messages
