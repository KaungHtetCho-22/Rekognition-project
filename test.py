import boto3
import json

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
    
    # Print out the response for debugging
    print("Index Faces Response:")
    print(json.dumps(response, indent=4, sort_keys=True))

    return response['FaceRecords']

def detect_faces(photo, bucket):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL']
    )
    
    # Print out the response for debugging
    print("Detect Faces Response:")
    print(json.dumps(response, indent=4, sort_keys=True))

    return response['FaceDetails']

def search_faces_by_image(photo, bucket, collection_id):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.search_faces_by_image(
        CollectionId=collection_id,
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MaxFaces=5,
        FaceMatchThreshold=70  # Lowered threshold for better matching
    )
    
    # Print out the response for debugging
    print("Search Faces by Image Response:")
    print(json.dumps(response, indent=4, sort_keys=True))

    return response['FaceMatches']

def main():
    index_photo = 'index/image1.jpg'
    group_photo = 'index/sample_images/team_photo.jpg'
    bucket = 'kaung-test-bucket'
    collection_id = 'Kaung-Test-Collection'
    external_image_id = 'person_1'

    # Index the face
    indexed_faces = index_face(index_photo, bucket, collection_id, external_image_id)
    if not indexed_faces:
        print("No faces were indexed. Please check the input image.")
        return

    # Detect faces in the group photo
    faces = detect_faces(group_photo, bucket)
    print(f"Detected {len(faces)} faces")

    if not faces:
        print("No faces detected in the group photo.")
        return

    # Search for the indexed face in the group photo
    matches = search_faces_by_image(group_photo, bucket, collection_id)
    if matches:
        for match in matches:
            print("Match found:")
            print(json.dumps(match, indent=4, sort_keys=True))
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
