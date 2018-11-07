import urllib.parse
import boto3
from biz.css.emotion_recognition import SatisfactionScore
from biz.css.reduction import apply_reduction
import biz.manage_restaurant as mr
import biz.css.file_storage as fs
from psycopg2 import pool
import config

print('Loading function')
s3 = boto3.client('s3')
conn = config.connection_string()
pool = pool.ThreadedConnectionPool(1, 1, conn)


def __get_details(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    return (bucket, key)


def __generate_url(bucket, key):
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        ExpiresIn='60',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )


# second parameter is the context, but currently unused
def customer_satisfaction(event, _):
    bucket, key = __get_details(event)
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
        url = __generate_url(bucket, key)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.\
         Make sure they exist and your bucket is in the \
         same region as this function.'.format(key, bucket))
        raise e

    print('detecting from url:{}.'.format(url))
    css = SatisfactionScore().detect_from_url(url)
    print(css)
    reduced = apply_reduction(css)
    print(reduced)

    conn = pool.getconn()
    try:
        mr.put_satisfaction(conn, (eid, rid), reduced)
    finally:
        pool.putconn(conn)
