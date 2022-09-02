# rekognition-client
A client to help you with AWS's Rekognition software

## Setup
- Install python dependencies
<pre>python3 install -r requirements.py</pre>

You're now good to go!

## Usage

- Upload images to S3 Bucket
<pre>python3 rekognize.py upload --image-data [PATH TO imageData.json] --bucket [BUCKET NAME]</pre>

- Detect faces in an image
<pre>python3 rekognize.py --filename [] --path [] --detectBucket [] --search-bucket [] --table-name [] --dest []</pre>
`--filename` - Name of input file <br>
`--path` - Path to folder containing file <br>
`--detect-bucket` - Bucket for temporarily storing input image <br>
`--search-bucket` - Bucket for looking through reference images <br>
`--table-name` - DynamoDB table used to store info for reference images <br>
`--dest` - Destination folder for matching faces
