import argparse

from packages.detect_faces import FaceRecognition
from packages.upload_to_bucket import upload_images

def find_matches(args):
    fr = FaceRecognition(
            filename=args.filename,
            imagePath=args.path,
            detectBucket=args.detect_bucket,
            searchBucket=args.search_bucket,
            tableName=args.table_name,
            destinationFolder=args.dest
        )
    faces = fr.detectFaces()
    key = 1
    if len(faces) > 0:
        print(f'\n{len(faces)} faces found.')
        for face in faces:
            match = fr.findMatches(face, key)
            if match != None:
                print(f'\nMatch {key}:',match['FaceId']['Item']['FullName']['S'])
                print('Confidence:', str(round(match['Match']['Similarity'], 3))+'%')
                key += 1
    else: print('No matches found!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('options', type=str, help="")

    # Optional arguments for uploading images
    parser.add_argument('-i', '--image-data', type=str)
    parser.add_argument('-b', '--bucket', type=str)

    # Optional arguments for detecting faces
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-p', '--path', type=str)
    parser.add_argument('-db', '--detect-bucket', type=str)
    parser.add_argument('-sb', '--search-bucket', type=str)
    parser.add_argument('-t', '--table-name', type=str)
    parser.add_argument('-d', '--dest', type=str)

    args = parser.parse_args()
    if args.options == 'upload':
        upload_images(info=args.image_data, bucket=args.bucket)
    elif args.options == 'detect':
        find_matches(args)


if __name__ == '__main__':
    main()
