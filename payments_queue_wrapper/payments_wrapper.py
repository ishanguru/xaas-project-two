import boto3
import ConfigParser

config_file_path = os.environ['LAMBDA_TASK_ROOT'] + '/configurations.txt'

config = ConfigParser.ConfigParser()
config.readfp(open(config_file_path))

awsAccessKey=config.get('AWS Keys', 'awsAccessKeyId')
awsSecretKey=config.get('AWS Keys', 'awsSecretAccessKeyId')
awsRegion=config.get('AWS Keys', 'awsRegion')

aws_session = Session(
    aws_access_key_id=awsAccessKey,
    aws_secret_access_key=awsSecretKey,
    region_name=awsRegion,
)

try:
	sqs_queue = aws_session.client('sqs')
except Exception as e:
    print("Queue already exists")

def payments_handler(event, context):
	queue_url = sqs_queue.get_queue_url(QueueName='ordersQueue')
	sqs_queue.receive_message(
		QueueUrl=queue_url
	)	
