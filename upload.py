import boto3

s3 = boto3.resource('s3')

images = [
    ('media/Elon_Musk_2015.jpg', 'Elon Musk'),
    ('media/Elon_Musk_Royal_Society_(crop2).jpg', 'Elon Musk'),
    ('media/SpaceX_CEO_Elon_Musk_visits_N&NC_and_AFSPC_(190416-F-ZZ999-006)_(cropped).jpg', 'Elon Musk'),
    ('media/IMG_0273.JPG', 'Abhisheke Acharya'),
    ('media/IMG_0337.JPG', 'Abhisheke Acharya'),
    ('media/IMG_0394.JPG', 'Abhisheke Acharya'),
    ('media/IMG_0584.JPG', 'Abhisheke Acharya'),
    ('media/IMG_1832.jpeg', 'Abhisheke Acharya'),
    ('media/Sundar_Pichai,_CEO,_Google_and_Alphabet_At_Singapore_FinTech_Festival.png', 'Sundar Pichai'),
    ('media/Sundar_pichai.png', 'Sundar Pichai'),
    ('media/Pichai_talks_about_AI_and_Tech.png', 'Sundar Pichai'),
    ('media/png-transparent-pewdiepie-youtuber-white-head-is-not-separated.png', 'Pewdiepie'),
    ('media/vfjx82feyn571.jpg', 'Pewdiepie'),
    ('media/PewDiePie-PNG-Isolated-Pic.png', 'Pewdiepie'),
]

for image in images:
    file = open(image[0], 'rb')
    object = s3.Object('blrpd-frs-demo', image[0])
    ret = object.put(Body=file, Metadata={'Fullname': image[1]})
