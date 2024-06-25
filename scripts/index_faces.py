import boto3
import os

def index_face_and_store_info(bucket, photo, collection_id, table_name):
    rekognition_client = boto3.client('rekognition')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    try:
        # Get metadata from S3 object
        s3_client = boto3.client('s3')
        response = s3_client.head_object(Bucket=bucket, Key=photo)
        metadata = response.get('Metadata', {})
        
        if not metadata:
            print("No metadata found. Exiting.")
            return

        # Create a valid ExternalImageId
        external_image_id = os.path.splitext(os.path.basename(photo))[0]  # Use filename without extension
        external_image_id = ''.join(c for c in external_image_id if c.isalnum() or c in ['_', '.', '-', ':'])
        print(f"Using ExternalImageId: {external_image_id}")

        # Index face
        response = rekognition_client.index_faces(
            CollectionId=collection_id,
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            ExternalImageId=external_image_id,
            DetectionAttributes=['ALL']
        )

        # Store information in DynamoDB
        face_records = response.get('FaceRecords', [])
        if not face_records:
            print("No faces indexed. Exiting.")
            return

        for face in face_records:
            face_id = face['Face']['FaceId']
            table.put_item(
                Item={
                    'RekognitionId': face_id,  # Use FaceId as the primary key
                    'face_id': face_id,
                    'name': metadata.get('name', ''),
                    'position': metadata.get('position', ''),
                    'nationality': metadata.get('nationality', ''),
                    'transfer_fees': metadata.get('transfer_fees', ''),
                    's3_object_key': photo,
                    'external_image_id': external_image_id
                }
            )
        
        print(f"Indexed face and stored info for {photo}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
index_face_and_store_info("kaung-test-bucket", "sample_images/image3.jpg", "kaung-test-collection", "kaung-testTable")
