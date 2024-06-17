import boto3

s3 = boto3.resource('s3')

images = [
    # ('image1.jpg', 'Allison Becker'),
    # ('image2.jpg', 'Andy Robertson'),
    # ('image3.jpg', 'Mac Allister'),
    # ('image4.jpg', 'Mohamad Salah'),
    # ('image5.jpg', 'Trent Arnold'),
    # ('image6.jpg', 'Van Dijki'),
    # ('image16.jpg', 'Boss'), # This is the cat photo, it will not be recognized
    # ('image20.jpg', 'Jurgen Klopp'),
    # ('image24.jpg', 'Hp'),
    ('sample_images/team_photo.jpg', 'team')
]

print('start uploading')
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('kaung-test-bucket','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})
print('end uploading')