"""
Adapter for the microsoft face recignition

Author: David Niwczyk and Robin Wohlers-Reichel
Date: 11/11/2018
"""

import cognitive_face as CF
import config


def detect_from_url(url):  # pragma: no cover
    """
    Hit the CF api for the image at 'url'.
    """
    KEY = config.cf_api_key()
    BASE = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    CF.Key.set(KEY)
    CF.BaseUrl.set(BASE)
    return CF.face.detect(url, True, False, 'emotion,glasses')
