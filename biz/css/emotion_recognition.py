import cognitive_face as CF
import config


def detect_from_url(url):  # pragma: no cover
    KEY = config.cf_api_key()
    BASE = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    CF.Key.set(KEY)
    CF.BaseUrl.set(BASE)
    return CF.face.detect(url, True, False, 'emotion,glasses')
