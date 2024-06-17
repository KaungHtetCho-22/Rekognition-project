import boto3

client = boto3.client('rekognition')

response = client.create_collection(CollectionId='kaung-test-collection')
print('Collection ARN: ' + response['CollectionArn'])
print('Status code: ' + str(response['StatusCode']))