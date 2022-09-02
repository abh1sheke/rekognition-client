import boto3
import io
from PIL import Image


# Variable Description
# imagePath - Path to folder that holds the image
# detectBucket - S3 bucket to temporarily store the image to be detected
# searchBucket - S3 bucket containing reference collection
# tableName - DynamoDB Table name to reference (table that contains searchBucket info)
# destinationFolder - Folder used to store matched faces

class FaceRecognition:
    def __init__(self, filename, imagePath, detectBucket, searchBucket, tableName, destinationFolder) -> None:
        self.filename = filename
        self.imagePath = imagePath

        # Saving image in RGB format
        self.image = Image.open(f'{imagePath}/{filename}')
        self.image = self.image.convert('RGB')
        self.detectBucket = detectBucket
        self.searchBucket = searchBucket
        self.tableName = tableName
        self.destinationFolder = destinationFolder

    def detectFaces(self):
        # Temporarily storing provided image
        s3 = boto3.resource('s3')
        file = open(self.imagePath, 'rb')
        object = s3.Object(self.detectBucket, self.filename)
        insert_image = object.put(
            Body=file, Metadata={'filename': self.filename})

        # Detecting all faces in provided image
        rekognition = boto3.client(
            'rekognition', region_name='ap-south-1')
        response = rekognition.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": self.detectBucket,
                    "Name": self.filename,
                }
            },
        )
        width, height = self.image.size
        images = []
        # Storing faces in a list
        for face in response['FaceDetails']:
            if face['Confidence'] > 90:
                box = face['BoundingBox']
                left = round(box['Left'] * width, 3)
                right = round((box['Left'] + box['Width']) * width, 3)
                top = round(box['Top'] * height, 3)
                bottom = round((box['Top'] + box['Height']) * height, 3)
                cropped_image = self.image.crop((left, top, right, bottom))
                images.append(cropped_image)
        return images

    def findMatches(self, face, key):
        # Getting image as bytes
        stream = io.BytesIO()
        face.save(stream, format='JPEG')
        imageBinary = stream.getvalue()

        # Cross referencing DynamoDB and reference collection
        dynamodb = boto3.client('dynamodb', region_name='ap-south-1')
        rekognition = boto3.client(
            'rekognition', region_name='ap-south-1')
        response = rekognition.search_faces_by_image(
            CollectionId=self.searchBucket,
            Image={
                'Bytes': imageBinary
            }
        )

        # Returning all matches
        for match in response['FaceMatches']:
            face_key = dynamodb.get_item(
                TableName=self.tableName,
                Key={
                    'RekognitionId': {'S': match['Face']['FaceId']}
                }
            )
            if 'Item' in face_key:
                face.save(
                    f'{self.destinationFolder}/images/{key}{self.filename}', format='JPEG')
                return {'Match': match, 'FaceId': face_key, 'MatchFile': f'{key}{self.filename}'}
        return None
