# SQS Message Retriever
Simple app to get messages from an SQS queue without deleting it and then visualize the data in a sortable table.

<sup>1) Make sure you have an AWS profile setup for the AWS environment you want to pull SQS messages from.</sup>

<sup>2) Ensure you have Python and flask setup and running locally.</sup>

Run the following command:

`env FLASK_ENV=development, FLASK_APP=main.py flask run`

The UI should be available at: `http://127.0.0.1:5000`
