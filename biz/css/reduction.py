from biz.css.random_forest import load_RF_File

negative_emotions = ['anger', 'contempt', 'disgust', 'fear', 'sadness']


def apply_reduction(raw_results):
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
    return prediction if prediction < 100 else 100
