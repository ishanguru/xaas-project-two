import boto3

class SQSServices():
	
	def __init__(self):
		print('Initializing SQS Service')
		self.sqs = boto3.resource('sqs')

	def createQueue(name):
		return self.sqs.create_queue(QueueName=name)

	def getQueueName(self, name, account):
		queueName = self.sqs.get_queue_by_name(QueueName=name, QueueOwnerAWSAccountId=account)
		return queueName

	def sendMessage(queueName, message):
		response = queueName.send_message(MessageBody=message)
		return response

	def receiveMessage(queueName, messageAttribute):
		return queueName.receive_messages(MessageAttributeNames=[messageAttribute])