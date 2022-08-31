from mailcap import findmatch
import boto3
import io
from PIL import Image
import os


class FaceRecognition:
    def __init__(self, filename, imagePath, detectBucket, searchBucket, tableName) -> None:
        self.filename = filename
        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self.detectBucket = detectBucket
        self.searchBucket = searchBucket
        self.tableName = tableName
        self.s3 = boto3.resource('s3')
        self.dynamodb = boto3.client('dynamodb', region_name='ap-south-1')
        self.rekognition = boto3.client(
            'rekognition', region_name='ap-south-1')

    def detectFaces(self):
        s3 = boto3.resource('s3')
        file = open(self.imagePath, 'rb')
        object = s3.Object(self.detectBucket, self.filename)
        ret = object.put(Body=file, Metadata={'filename': self.filename})
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
        for face in response['FaceDetails']:
            if face['Confidence'] > 90:
                box = face['BoundingBox']
                left = round(box['Left'] * width, 3)
                right = round((box['Left'] + box['Width']) * width, 3)
                top = round(box['Top'] * width, 3)
                bottom = round((box['Top'] + box['Height']) * height, 3)
                cropped_image = self.image.crop((left, top, right, bottom))
                images.append(cropped_image)
        return images

    def findMatches(self, face):
        stream = io.BytesIO()
        face.save(stream, format='JPEG')
        imageBinary = stream.getvalue()

        response = self.rekognition.search_faces_by_image(
            CollectionId=self.searchBucket,
            Image={
                'Bytes': imageBinary
            }
        )

        for match in response['FaceMatches']:
            print(match)
            face = self.dynamodb.get_item(
                TableName=self.tableName,
                Key={
                    'RekognitionId': {'S': match['Face']['FaceId']}
                }
            )
            if 'Item' in face:
                return face
        return None


if __name__ == '__main__':
    faceRec = FaceRecognition(
        filename='102859427-pewdiepieez.jpg',
        imagePath='./media/102859427-pewdiepie.jpg',
        detectBucket='detect-face',
        searchBucket='blrpd-frs-demo',
        tableName='blrpd-frs-demo'
    )
    images = faceRec.detectFaces()
    matches = []
    for image in images:
        match = faceRec.findMatches(image)
        if match != None:
            matches.append(match)
    print(matches)
