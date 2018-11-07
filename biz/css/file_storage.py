"""
Functions for accessing files in blob storage.

Author: Andrew Pope, Big Rob
Date: timeless
"""

import base64
import boto3
import io


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


def upload_base64(filename, photo):
    b64 = photo.split(',')[1]
    decoded = io.BytesIO(base64.b64decode(b64))
    s3 = boto3.client('s3')
    s3.upload_fileobj(decoded, "irs-images", filename)
