import cognitive_face as CF


def detect_from_url(url):  # pragma: no cover
    KEY = 'fcef05be3b9f440f9e38dfb675b07de6'
    BASE = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
    CF.Key.set(KEY)
    CF.BaseUrl.set(BASE)
    return CF.face.detect(url, True, False, 'emotion,glasses')
