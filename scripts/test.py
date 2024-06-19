import boto3
import re

def detect_faces(photo, bucket):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL']
    )
    return response['FaceDetails']

def index_faces(photo, bucket, collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    # Sanitize ExternalImageId
    sanitized_external_image_id = re.sub(r'[^a-zA-Z0-9_.\-:]', '_', photo)

    response = rekognition_client.index_faces(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        ExternalImageId=sanitized_external_image_id,
        DetectionAttributes=['ALL']
    )
    return response['FaceRecords']

def search_faces_by_image(photo, bucket, collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.search_faces_by_image(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        FaceMatchThreshold=95,
        MaxFaces=1
    )
    return response['FaceMatches']

# Define your S3 bucket and image paths
team_photo = 'index/sample_images/team_photo.jpg'
individual_photo = 'index/image2.jpg'
bucket = 'kaung-test-bucket'
collection_id = 'kaung-test-collection'

# Index faces in the team photo
# team_faces = index_faces(team_photo, bucket, collection_id)
# print(f"Indexed {len(team_faces)} faces from team photo")

# Search for the individual face in the collection
face_matches = search_faces_by_image(individual_photo, bucket, collection_id)

if face_matches:
    matched_face_id = face_matches[0]['Face']['FaceId']
    print(f"Matched FaceId: {matched_face_id}")
    print(f"The face in {individual_photo} is included in {team_photo}")
else:
    print("No matching face found")
    print(f"The face in {individual_photo} is not included in {team_photo}")
