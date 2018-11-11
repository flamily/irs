"""
Lambda which converts images into css
Triggers on s3 bucket event
Upload the image to Azure
Put the CSS into the db

Author: Robin Wohlers-Reichel
Date: 11/11/2018
"""

import urllib.parse
import boto3
import biz.css.emotion_recognition as er
import biz.css.reduction as r
import biz.css.manage_satisfaction as ms
import biz.css.file_storage as fs
from psycopg2 import pool
import config

print('Loading function')
s3 = boto3.client('s3')
__pool = None


def get_pool_lazy():  # pragma: no cover
    """
    Get a database pool, but in a way we can override for tests
    """
    # pylint: disable=global-statement
    global __pool
    if __pool is None:
        __pool = pool.ThreadedConnectionPool(1, 1, config.connection_string())
    return __pool


def get_details(event):
    """
    Get details of the event being passed into the lambda

    :param event: Event object passed into the lambda
    :return: Name of the bucket and key of file (filename)
    """
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    return (bucket, key)


def generate_url(s3client, bucket, key):  # pragma: no cover
    """
    Generate a short-lived public url for the specified key

    :param s3client: AWS S3 client to use to generate url
    :param bucket: The bucket the object resides in
    :param key: The key of the object
    :return: Public url to the object
    """
    return s3client.generate_presigned_url(
        ClientMethod='get_object',
        ExpiresIn='60',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )


def css_for_image_at_url(url):
    """
    Calculate the css for an image at `url`

    :param url: The url to use
    :return: CSS score
    """
    css = er.detect_from_url(url)
    return r.apply_reduction(css)


def save_css(p, css, eid, rid):
    """
    Save the CSS to the database

    :param p: Database pool
    :param css: CSS Score
    :param eid: Event ID
    :param rid: Reservation ID
    """
    conn = p.getconn()
    try:
        ms.create_satisfaction(conn, css, eid, rid)
    finally:
        p.putconn(conn)


# second parameter is the context, but currently unused
def calculate_css_from_image(event, _):
    """
    The lambda event handler entry point

    :param event: Information about the trigger
    """
    bucket, key = get_details(event)
    eid = None
    rid = None
    try:
        eid, rid = fs.deconstruct_filename(key)
    except ValueError as e:
        print(e)
        print('Error deconstructing filename {} into \
        event id and reservation id.'.format(key))
        return

    print('eid={}, rid={}'.format(eid, rid))

    url = None
    try:
        url = generate_url(s3, bucket, key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.\
         Make sure they exist and your bucket is in the \
         same region as this function.'.format(key, bucket))
        raise e

    reduced = css_for_image_at_url(url)
    save_css(get_pool_lazy(), reduced, eid, rid)
