import boto3

def get_collection_arn(collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')
    response = rekognition_client.describe_collection(CollectionId=collection_id)
    return response['CollectionARN']

# Specify the collection ID
collection_id = 'kaung-test-collection'

collection_arn = get_collection_arn(collection_id)
print("Collection ARN:", collection_arn)
