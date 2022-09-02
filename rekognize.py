import argparse

from packages.detect_faces import FaceRecognition
from packages.upload_to_bucket import upload_images

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload_images', action='store_true')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
