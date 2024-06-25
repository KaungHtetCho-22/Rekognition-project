import boto3
import io
from PIL import Image, ImageDraw

def detect_faces(photo, bucket):
    session = boto3.Session(profile_name='default')
    rekognition_client = session.client('rekognition')

    response = rekognition_client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        Attributes=['ALL']
    )
    return response['FaceDetails']

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

def draw_bounding_box(image_bytes, bounding_box, expand_factor=0.5):
    image = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(image)

    width, height = image.size
    
    # Calculate the expansion amount
    expand_x = bounding_box['Width'] * width * expand_factor
    expand_y = bounding_box['Height'] * height * expand_factor

    # Expand the bounding box
    left = max(0, (bounding_box['Left'] * width) - expand_x)
    top = max(0, (bounding_box['Top'] * height) - expand_y)
    right = min(width, left + (bounding_box['Width'] * width) + (2 * expand_x))
    bottom = min(height, top + (bounding_box['Height'] * height) + (2 * expand_y))

    draw.rectangle([left, top, right, bottom], outline='red', width=3)

    return image

def get_image_from_s3(bucket, photo):
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=photo)
    return response['Body'].read()

def calculate_iou(box1, box2):
    # Calculate the Intersection over Union (IoU) of two bounding boxes
    x1 = max(box1['Left'], box2['Left'])
    y1 = max(box1['Top'], box2['Top'])
    x2 = min(box1['Left'] + box1['Width'], box2['Left'] + box2['Width'])
    y2 = min(box1['Top'] + box1['Height'], box2['Top'] + box2['Height'])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = box1['Width'] * box1['Height']
    area2 = box2['Width'] * box2['Height']
    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0

def main():
    team_photo = 'sample_images/ss_cody.jpg'
    individual_photo = 'sample_images/image1.jpg'
    bucket = 'kaung-test-bucket'
    collection_id = 'kaung-test-collection'

    # Search for the individual face in the collection
    face_matches = search_faces_by_image(individual_photo, bucket, collection_id)

    if face_matches:
        matched_face = face_matches[0]['Face']
        print(f"Matched FaceId: {matched_face['FaceId']}")
        print(f"The face in {individual_photo} is included in {team_photo}")

        # Get the bounding box of the matched face
        matched_bounding_box = matched_face['BoundingBox']

        # Detect faces in the team photo
        faces = detect_faces(team_photo, bucket)

        # Find the face with the closest matching bounding box
        best_match = None
        best_iou = 0
        for face in faces:
            iou = calculate_iou(matched_bounding_box, face['BoundingBox'])
            if iou > best_iou:
                best_iou = iou
                best_match = face

        if best_match:
            print(f"Bounding Box for matched face in team photo: {best_match['BoundingBox']}")
            
            # Get the team photo from S3
            team_photo_bytes = get_image_from_s3(bucket, team_photo)
            
            # Draw bounding box on the image
            image_with_box = draw_bounding_box(team_photo_bytes, best_match['BoundingBox'])
            
            # Save the image with bounding box
            output_path = 'team_photo_with_box.jpg'
            image_with_box.save(output_path)
            print(f"Image with bounding box saved as {output_path}")
        else:
            print("Matched face not found in the team photo")
    else:
        print("No matching face found")
        print(f"The face in {individual_photo} is not included in {team_photo}")

if __name__ == "__main__":
    main()