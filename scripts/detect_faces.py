import boto3

def detect_faces(photo, bucket):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL']
    )
    return response['FaceDetails']

photo = 'index/sample_images/team_photo.jpg'
bucket = 'kaung-test-bucket'

faces = detect_faces(photo, bucket)
print(f"Detected {len(faces)} faces")
