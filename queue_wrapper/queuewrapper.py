from sqs_services import SQSServices
import boto3
import json

try:
	sqs_queue = SQSServices()
except Exception as e:
	print("Queue exists")

def lambda_handler(event, trigger):
	if event['type'] == 'accountsQuery':
		response = processAccountsData(event)
	elif event['type'] == 'informationQuery':
		response = processCustomerData(event)
	elif event['type'] == 'paymentsQuery':
		response = processPaymentsData(event)
	else:
		response = {'error': "Not a valid query type"}
	return json.loads(response)

def processAccountsData(event):
	queue_name = sqs_queue.getQueueName('authenticationQueue')
	response = []
	for message in queue_name.receive_messages(MessageAttributeNames=['email']):
        json_dict = json.loads(message.body)
        if event['jwt'] == json_dict['jwt']:
        	response.append(message)
    return response
    
def processCustomerData(event):
	queue_name = sqs_queue.getQueueName('informationQueue')
	response = []
	for message in queue_name.receive_messages(MessageAttributeNames=['email']):
        json_dict = json.loads(message.body)
        if event['jwt'] == json_dict['jwt']:
        	response.append(message)
    return response

def processPaymentsData(event):
	queue_name = sqs_queue.getQueueName('paymentsQueue')
	response = []
	for message in queue_name.receive_messages(MessageAttributeNames=['email']):
        json_dict = json.loads(message.body)
        if event['jwt'] == json_dict['jwt']:
        	response.append(message)
    return response
