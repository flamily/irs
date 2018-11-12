"""
Author: Joshua De los Santos
Modified: 10:38PM - 12/11/2018

Description:
    Methods to reduce azure data into a single satisfaction number.
"""
import pickle
import config

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
    to_predict = list(emotions.values())
    to_predict_str = ['{:.3f}'.format(x) for x in to_predict]
    prediction = bagging_predict(model, to_predict_str) * 10
    return int(prediction) if int(prediction) < 100 else 100


def bagging_predict(trees, row):
    """Make a prediction with a list of bagged trees

    :param trees: a list of the random forest trees
    :param row: entry of data to be classified
    :return: predicted data
    """
    predictions = [predict(tree, row) for tree in trees]
    return max(set(predictions), key=predictions.count)


def predict(node, row):
    """Make a prediction with a single decision tree

    :param node: a tree
    :param row: entry of data to be classified
    :return: predicted data
    """
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']


def load_RF_File():
    """Load .pkl model file
    :return: classifier object
    """
    with open('RF_list.pkl', 'rb') as model_file:
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
