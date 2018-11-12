"""
Functions for accessing files in blob storage.

Author: Andrew Pope, Big Rob
Date: timeless
"""

import base64
import boto3
import io
import config


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


def bucket_upload(img, event_id, reservation_id):  # pragma: no cover
    filename = construct_filename(event_id, reservation_id)
    if config.is_running_on_lambda():
        b64 = img.split(',')[1]
        decoded = io.BytesIO(base64.b64decode(b64))
        s3 = boto3.client('s3')
        s3.upload_fileobj(decoded, "irs-images", filename)
    else:
        print("Not running on lambda. \
        Mocking sent image event={}, reservation={}, \
        encoded img len={}".format(event_id, reservation_id, len(img)))


def bucket_download(bucket, key):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    res = obj.get()
    return res['Body'].read()
