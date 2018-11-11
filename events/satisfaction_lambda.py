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
conn = config.connection_string()
__pool = None


def get_pool_lazy():  # pragma: no cover
    global __pool
    if __pool is None:
        __pool = pool.ThreadedConnectionPool(1, 1, conn)
    return __pool


def get_details(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    return (bucket, key)


def generate_url(s3client, bucket, key):  # pragma: no cover
    return s3client.generate_presigned_url(
        ClientMethod='get_object',
        ExpiresIn='60',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )


def css_for_image_at_url(url):
    print('detecting from url:{}.'.format(url))
    css = er.detect_from_url(url)
    return r.apply_reduction(css)


def save_css(pool, css, eid, rid):
    conn = pool.getconn()
    try:
        ms.create_satisfaction(conn, css, eid, rid)
    finally:
        pool.putconn(conn)


# second parameter is the context, but currently unused
def customer_satisfaction(event, _):
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
