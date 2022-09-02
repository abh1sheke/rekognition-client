import json
import boto3
from tqdm import tqdm

def upload_images(info, bucket):
    # Loading S3 client
    s3 = boto3.resource('s3')

    # Extracting image info from imageData.json
    print('Extracting image data...')
    with open(info, 'r') as f:
        data = json.load(f)
        path = data['path']
        images = data['images']

    # Uploading images to specified S3 bucket
    print('Uploading images...')
    for image in tqdm(images):
        filename = image['filename']
        image_file = open(f'{path}/{filename}', 'rb')
        # Creating S3 Object and inserting file into specified bucket
        s3_object = s3.Object(bucket, f'media/{filename}')
        insert = s3_object.put(Body=image_file, Metadata={
                               'FullName': image['personName'], 'Filename': filename})
    print('Uploaded all images successfully.')
