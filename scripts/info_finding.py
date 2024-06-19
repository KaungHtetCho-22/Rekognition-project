import boto3

def describe_collection(collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')
    
    response = rekognition_client.describe_collection(CollectionId=collection_id)
    
    return response

collection_id = 'kaung-test-collection'

collection_info = describe_collection(collection_id)

print("Collection ARN:", collection_info['CollectionARN'])
print("Face Count:", collection_info['FaceCount'])
print("Creation Timestamp:", collection_info['CreationTimestamp'])