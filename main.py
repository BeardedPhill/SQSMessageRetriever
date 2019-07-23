from flask import Flask, escape, request, render_template
from message import Message, PageData
import sys
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('get_messages_form.html', pageData=buildPageData('', 10))

@app.route("/get_sqs_messages", methods=["POST"])
def get_messages():
    for key, value in request.form.items():
        if (key=="SQS_URL"):
            queue_url_global=value
            queue_url = value
        elif (key=="MAX_MSG"):
            max_messages_global=int(value)
            max_messages = int(value)

    try:
        messages = call_sqs(queue_url, max_messages)
        return render_template(
            'index.html',
            messages=messages,
            pageData=buildPageData(queue_url, max_messages)
        )
    except Exception as e:
        return render_template(
            'error_template.html',
            error_message=str(e),
            pageData=buildPageData(queue_url, max_messages)
        )

def buildPageData(queue_url, max_messages):
    return PageData(queue_url, max_messages)

def get_messages_from_queue(queue_url, max_messages):
    sqs_client = boto3.client('sqs')
    max_messages_per_api_call=10
    message_count=0

    while True:
        if message_count < max_messages:
            max_messages_per_api_call = determine_max_message_count(
                message_count,
                max_messages_per_api_call,
                max_messages
            )

            resp = sqs_client.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                VisibilityTimeout=2,
                MaxNumberOfMessages=max_messages_per_api_call
            )

            try:
                message_count += len(resp['Messages'])

                for message in resp['Messages']:
                    yield message
            except KeyError:
                return
        else:
            return

def determine_max_message_count(
    current_message_count,
    max_messages_per_api_call,
    max_messages_to_return_in_total):

    left_over_messages_to_retrieve_count = max_messages_to_return_in_total - current_message_count

    if left_over_messages_to_retrieve_count < max_messages_per_api_call:
        return left_over_messages_to_retrieve_count
    else:
        return max_messages_per_api_call


def call_sqs(queue_url, max_messages):
    messages=[]
    for message in get_messages_from_queue(queue_url, max_messages):
        messages.append(Message(message))

    return messages
