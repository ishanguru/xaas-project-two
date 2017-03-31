from sqs_services import SQSServices
import boto3
import json
import boto
import boto.sqs

try:
    sqs_queue = SQSServices()
except Exception as e:
    print("Queue exists")


def lambda_handler(event, trigger):
    if event['type'] == 'signupQuery':
        response = processSignupData(event)
    elif event['type'] == 'loginQuery':
        response = processLoginData(event)
    elif event['type'] == 'paymentsQuery':
        response = processPaymentsData(event)
    else:
        response = {'error': "Not a valid query type"}
    return response


def processSignupData(event):
    conf = {"sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
            "sqs-secret-key": "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",
            "sqs-queue-name": "queue_signup",
            "sqs-region": "us-east-1",
            "sqs-path": "sqssend"
            }

    conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id=conf.get('sqs-access-key'),
        aws_secret_access_key=conf.get('sqs-secret-key')
    )

    queue = conn.get_queue('queue_signup')
    response = []

    for message in queue.get_messages():
        print str(message.get_body())
        response.append(str(message.get_body()))

    return response


def processLoginData(event):
    conf = {"sqs-access-key": "AKIAJN3ACGV3J6SG3Q5A",
            "sqs-secret-key": "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",
            "sqs-queue-name": "queue_login",
            "sqs-region": "us-east-1",
            "sqs-path": "sqssend"

            }

    conn = boto.sqs.connect_to_region(
        conf.get('sqs-region'),
        aws_access_key_id=conf.get('sqs-access-key'),
        aws_secret_access_key=conf.get('sqs-secret-key')
    )

    queue = conn.get_queue('queue_login')
    response = []

    for message in queue.get_messages():
        response.append(message)

    return response


def processCustomerData(event):
    queue_name = sqs_queue.getQueueName('informationQueue')
    response = []
    for message in queue_name.get_messages():
        json_dict = json.loads(message.body)
    if event['jwt'] == json_dict['jwt']:
        response.append(message)

    return response


def processPaymentsData(event):
    queue_name = sqs_queue.getQueueName('paymentsQueue')
    response = []
    for message in queue_name.get_messages():
        json_dict = json.loads(message.body)
    if event['jwt'] == json_dict['jwt']:
        response.append(message)

    return response
