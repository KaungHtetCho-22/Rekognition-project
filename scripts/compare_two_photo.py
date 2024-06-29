import boto3

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

def get_face_info_from_dynamodb(face_id, table_name):
    session = boto3.Session(profile_name='default')
    dynamodb = session.resource('dynamodb')
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={'RekognitionId': face_id})
    return response.get('Item', {})

def main():
    test_photo = 'sample_images/image2.jpg'
    reference_photo = 'sample_images/image2.jpg'
    bucket = 'kaung-test-bucket'
    collection_id = 'kaung-test-collection'
    dynamodb_table = 'kaung-testTable'

    # Search for the reference face in the collection to get the RekognitionId
    reference_matches = search_faces_by_image(reference_photo, bucket, collection_id)

    if reference_matches:
        reference_face_id = reference_matches[0]['Face']['FaceId']
        reference_confidence = reference_matches[0]['Similarity']

        # Get and print reference face info from DynamoDB
        reference_face_info = get_face_info_from_dynamodb(reference_face_id, dynamodb_table)
        print("Reference Face Information:")
        for key, value in reference_face_info.items():
            print(f"{key}: {value}")

        # Search for the test face in the collection
        test_matches = search_faces_by_image(test_photo, bucket, collection_id)

        if test_matches:
            matched_face = test_matches[0]['Face']
            test_confidence = test_matches[0]['Similarity']

            # Get and print test face info from DynamoDB
            test_face_info = get_face_info_from_dynamodb(matched_face['FaceId'], dynamodb_table)
            print("\nTest Face Information:")
            for key, value in test_face_info.items():
                print(f"{key}: {value}")

            if matched_face['FaceId'] == reference_face_id:
                print("\nThe test face matches the reference face.")
                print(f"Matching confidence: {test_confidence:.2f}%")
            else:
                print("\nThe test face does not match the reference face.")
        else:
            print("\nNo matching face found")
            print(f"The face in {test_photo} is not included in the collection")
    else:
        print("\nNo matching reference face found")
        print(f"The face in {reference_photo} is not included in the collection")

if __name__ == "__main__":
    main()
