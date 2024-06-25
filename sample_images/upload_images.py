import os
import boto3

def upload_image_to_s3(file_path, bucket, object_name, metadata):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, object_name, 
                              ExtraArgs={"Metadata": metadata})
        print(f"Successfully uploaded {object_name} to {bucket}")
        return True
    except Exception as e:
        print(f"Error uploading file {object_name}: {e}")
        return False

def upload_multiple_images(image_folder, bucket, player_data):
    successful_uploads = 0
    failed_uploads = 0

    for player in player_data:
        file_name = player['file_name']
        file_path = os.path.join(image_folder, file_name)
        object_name = f"sample_images/{file_name}"

        metadata = {
            "name": player['name'],
            "position": player['position'],
            "nationality": player['nationality'],
            "transfer_fees": str(player['transfer_fees'])
        }

        if upload_image_to_s3(file_path, bucket, object_name, metadata):
            successful_uploads += 1
        else:
            failed_uploads += 1

    print(f"Upload complete. Successful: {successful_uploads}, Failed: {failed_uploads}")

# Usage example
player_data = [
    {
        "file_name": "image1.jpg",
        "name": "Allison",
        "position": "Goal",
        "nationality": "Brasil",
        "transfer_fees": 50000000
    },
    {
        "file_name": "image2.jpg",
        "name": "Robertson",
        "position": "Defender",
        "nationality": "Scotland",
        "transfer_fees": 40000000
    },
    {
        "file_name": "image3.jpg",
        "name": "Allister",
        "position": "Midfielder",
        "nationality": "Argentina",
        "transfer_fees": 35000000
    },
    {
        "file_name": "image20.jpg",
        "name": "Jurgen",
        "position": "Coach",
        "nationality": "Germany",
        "transfer_fees": 765000000
    }
]

image_folder = ""
bucket_name = "kaung-test-bucket"

upload_multiple_images(image_folder, bucket_name, player_data)