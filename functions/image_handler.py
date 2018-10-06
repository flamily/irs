import json
import urllib.parse
import boto3
import os
import cognitive_face as CF

print('Loading function')
s3 = boto3.client('s3')

def emotion_recognition(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            ExpiresIn='10',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )

        CF.BaseUrl.set(os.environ['EMOTION_API_BASE_URL'])
        CF.Key.set(os.environ['EMOTION_API_KEY'])
        face = CF.face.detect(url)
        print(face)

        return face
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e