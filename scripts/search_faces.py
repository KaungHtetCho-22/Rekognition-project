import boto3

def search_faces_by_image(photo, bucket, collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.search_faces_by_image(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MaxFaces=5,
        FaceMatchThreshold=85
    )
    return response['FaceMatches']

photo = 'index/sample_images/team_photo.jpg'
collection_id = 'kaung-test-collection'
bucket = 'kaung-test-bucket'

matches = search_faces_by_image(photo, bucket, collection_id)
for match in matches:
    print(match)