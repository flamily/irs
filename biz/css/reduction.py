"""
Author: Joshua De los Santos
Modified: 12:12PM - 12/11/2018

Description:
    Methods to reduce azure data into a single satisfaction number.
"""
import pickle
import config
import biz.css.file_storage as fs

negative_emotions = ['anger', 'contempt', 'disgust', 'fear', 'sadness']


def apply_reduction(raw_results):
    """Apply Random Forest prediction to azure json data

    :param raw_results: azure json data
    :return: satisfaction percentage between 0 and 100
    """
    try:
        raw_results[0]["faceAttributes"]["emotion"]
    except (ValueError, IndexError, TypeError):
        return -1

    emotions = {
        'anger': 0.0,
        'contempt': 0.0,
        'disgust': 0.0,
        'fear': 0.0,
        'happiness': 0.0,
        'neutral': 0.0,
        'sadness': 0.0,
        'surprise': 0.0
    }
    for face in raw_results:
        for emotion in face["faceAttributes"]["emotion"]:
            emotions[emotion] += (face["faceAttributes"]["emotion"][emotion])
    for emotion in emotions:
        emotions[emotion] /= len(raw_results)
    emotion_weight_key = max(emotions, key=emotions.get)
    emotion_weight = emotions[emotion_weight_key]
    if emotion_weight_key in negative_emotions:
        emotion_weight *= -1
    model = load_RF_File()
    to_predict = [list(emotions.values())]
    prediction = (model.predict(to_predict) + emotion_weight) * 10
    return prediction[0] if prediction[0] < 100 else 100


def load_RF_File():
    """Load .joblib model file
    :return: classifier object
    """
    if config.is_running_on_lambda():
        return __lazy_s3_model()  # pragma: no cover
    with open('biz/css/RF_model.pkl', 'rb') as model_file:
        return pickle.load(model_file)


_model = None


def __lazy_s3_model():  # pragma: no cover
    # pylint: disable=global-statement
    global _model
    if _model is None:
        print("Don't have the model yet. Have to load model from S3...")
        f = fs.bucket_download(
            config.model_bucket(),
            config.model_key(),
        )
        _model = pickle.loads(f)
    return _model
