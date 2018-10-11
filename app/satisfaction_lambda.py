import urllib.parse
import boto3
from app/emotion_recognition import SatisfactionScore

print('Loading function')
s3 = boto3.client('s3')


def customer_satisfaction(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    try:

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            ExpiresIn='10',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )

        css = SatisfactionScore.detect_from_url(url)
        print(css)

        return css
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.\
         Make sure they exist and your bucket is in the \
         same region as this function.'.format(key, bucket))
        raise e
