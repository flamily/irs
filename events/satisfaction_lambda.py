"""
Functions for accessing blob storage and customer satisfaction.

Author: Robin Wohlers-Reichel, Andrew Pope
Date: 06/11/2018
"""
import urllib.parse
import boto3
from biz.css.emotion_recognition import SatisfactionScore
from biz.css.reduction import apply_reduction

print('Loading function')
s3 = boto3.client('s3')


def construct_filename(event_id, reservation_id, extension='img'):
    """Generate a customer event filename for blob storage.

    :param event_id: The database ID of an event record.
    :param reservation_id: The database ID of a reservation record.
    :param extension: Optional filename extension specifier.
    :return: A string containing the filename with extension.
    """
    if not isinstance(event_id, int):
        raise TypeError('event_id must be an int')
    if not isinstance(reservation_id, int):
        raise TypeError('reservation_id must be an int')

    return "{}-{}.{}".format(event_id, reservation_id, extension)


def deconstruct_filename(filename):
    """Deconstruct a blob storage filename into (event_id, reservation_id).

    :param filename: Can optionally contain the filename extension.
    :return: A tuple of (event_id, reservation_id)
    """
    decon = (filename.split('.')[0]).split('-')
    return (int(decon[0]), int(decon[1]))


# second parameter is the context, but currently unused
def customer_satisfaction(event, _):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    try:

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            ExpiresIn='600',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )

        print('detecting from url:{}.'.format(url))
        css = SatisfactionScore().detect_from_url(url)
        print(css)
        reduced = apply_reduction(css)
        print(reduced)

        return css
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.\
         Make sure they exist and your bucket is in the \
         same region as this function.'.format(key, bucket))
        raise e
