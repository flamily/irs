from random_forest import load_RF_File

negative_emotions = ['anger', 'contempt', 'disgust', 'fear', 'sadness']


def apply_reduction(raw_results):
    emotions = raw_results[0]["faceAttributes"]["emotion"]
    emotion_weight_key = max(emotions, key=emotions.get)
    emotion_weight = emotions[emotion_weight_key]
    if emotion_weight_key in negative_emotions:
        emotion_weight *= -1
    model = load_RF_File()
    to_predict = [list(emotions.values())]
    prediction = (model.predict(to_predict) + emotion_weight) * 10
    return prediction if prediction < 100 else 100
