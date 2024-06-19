import boto3

def index_face(photo, bucket, collection_id, external_image_id):
    
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.index_faces(
        CollectionId=collection_id,
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo,
            }
        },
        ExternalImageId=external_image_id,
        DetectionAttributes=['ALL']
    )
    return response['FaceRecords']

photo = 'index/image1.jpg'
bucket = 'kaung-test-bucket'
collection_id = 'kaung-test-collection'
external_image_id = 'jurgen klopp'

index_face(photo, bucket, collection_id, external_image_id)