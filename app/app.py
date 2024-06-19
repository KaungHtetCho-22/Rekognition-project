from flask import Flask, render_template, request, jsonify
import boto3
import io

app = Flask(__name__)

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    return jsonify({'status': 'success'})

@app.route('/recognize', methods=['POST'])
def recognize():
    # Get the image data from the request
    image_data = request.files['image'].read()

    # Use AWS Rekognition to search for faces in the image
    response = rekognition.search_faces_by_image(
        CollectionId='testCollection',
        Image={'Bytes': image_data}
    )

    # Process the response and return the recognition result
    result = process_recognition_response(response)
    return jsonify(result)

def process_recognition_response(response):
    found = False
    result = {'status': 'not_recognized'}

    for match in response.get('FaceMatches', []):
        face = dynamodb.get_item(
            TableName='testTable',
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )

        if 'Item' in face:
            result = {
                'status': 'recognized',
                'name': face['Item']['FullName']['S']
            }
            found = True
            break

    if not found:
        result['status'] = 'not_recognized'

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)