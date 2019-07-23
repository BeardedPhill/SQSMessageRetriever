from flask import Flask, escape, request, render_template, flash
from message import Message, SqsFormData
import sys
import boto3
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
sqs_client = boto3.client('sqs')

@app.route('/')
def index():
    return render_template('get_messages_form.html', sqsFormData=buildSqsFormData(request))

@app.route("/get_sqs_messages", methods=["POST"])
def get_messages():
    sqsFormData=buildSqsFormData(request)

    try:
        messages = call_sqs(sqsFormData.queue_url, sqsFormData.max_messages, sqsFormData.delete_messages)
        return render_template(
            'index.html',
            messages=messages,
            sqsFormData=sqsFormData
        )
    except Exception as e:
        return render_template(
            'error_template.html',
            error_message=str(e),
            sqsFormData=sqsFormData
        )

def buildSqsFormData(request):
    # Default values
    queue_url=''
    max_messages=10

    for key, value in request.form.items():
        if (key=="SQS_URL"):
            queue_url = value
        elif (key=="MAX_MSG"):
            max_messages = int(value)

    delete_messages = request.form.get("DEL_MSG")
    return SqsFormData(queue_url, max_messages, delete_messages)

def get_messages_from_queue(queue_url, max_messages, delete_messages):
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

            if delete_messages=='on':
                delete_messages_from_sqs(queue_url, resp)
        else:
            return

def delete_messages_from_sqs(queue_url, retrieve_response):
    entries=[]
    for msg in retrieve_response['Messages']:
        entries.append({'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']})

    delete_response = sqs_client.delete_message_batch(
        QueueUrl=queue_url, Entries=entries
    )

    try:
        flash_message = ("Failed to delete messages:" +
            "\nretrieved entries=" + repr(entries) +
            "\ndelete response=" + repr(delete_response)).split('\n')

        if len(delete_response['Successful']) != len(entries):
            flash(flash_message)
    except KeyError:
        flash(flash_message)

def determine_max_message_count(
    current_message_count,
    max_messages_per_api_call,
    max_messages_to_return_in_total):

    left_over_messages_to_retrieve_count = max_messages_to_return_in_total - current_message_count

    if left_over_messages_to_retrieve_count < max_messages_per_api_call:
        return left_over_messages_to_retrieve_count
    else:
        return max_messages_per_api_call


def call_sqs(queue_url, max_messages, delete_messages):
    messages=[]
    for message in get_messages_from_queue(queue_url, max_messages, delete_messages):
        messages.append(Message(message))

    return messages
