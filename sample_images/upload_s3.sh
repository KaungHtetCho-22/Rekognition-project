#!/bin/bash

# Define the path to the images and the S3 bucket name
image_folder="/home/koala/freelance projects/Rekognition project/sample_images"
bucket="kaung-test-bucket"

# Player data (manually input, could be automated with a configuration file or other means)
declare -A Allison=("file_name=image1.jpg" "name=Allison Becker" "position=goal_keeper" "nationality=Brasil" "transfer_fees=50000000")
declare -A Andy=("file_name=image2.jpg" "name=Andy Robertson" "position=left_defender" "nationality=Scotland" "transfer_fees=40000000")
declare -A Alliser=("file_name=image3.jpg" "name=Mac Allister" "position=DM" "nationality=Argentina" "transfer_fees=35000000")
declare -A Jurgen=("file_name=image20.jpg" "name=Jurgen Klopp" "position=Coach" "nationality=Germany" "transfer_fees=100000000")

# Array of players
players=(Allison Andy Alliser Jurgen)

successful_uploads=0
failed_uploads=0

# Function to upload a file to S3 with metadata
upload_image_to_s3() {
    local file_path=$1
    local bucket=$2
    local object_name=$3
    local metadata=$4

    # Construct metadata string for AWS CLI
    metadata_args=""
    for key in "${!metadata[@]}"; do
        metadata_args+="--metadata ${key}=${metadata[$key]} "
    done

    # AWS CLI command to upload the file
    if aws s3 cp "$file_path" "s3://$bucket/$object_name" $metadata_args; then
        echo "Successfully uploaded $object_name to $bucket"
        ((successful_uploads++))
    else
        echo "Error uploading file $object_name"
        ((failed_uploads++))
    fi
}

for player in "${players[@]}"; do
    declare -n player_data=$player
    file_name=${player_data[file_name]}
    file_path="$image_folder/$file_name"
    object_name="players/$file_name"

    # Upload the image
    upload_image_to_s3 "$file_path" "$bucket" "$object_name" player_data
done

echo "Upload complete. Successful: $successful_uploads, Failed: $failed_uploads"
