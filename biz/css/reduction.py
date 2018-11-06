from random_forest import load_RF_File

def apply_reduction(raw_results):
    emotions = raw_results[0]["faceAttributes"]["emotion"]
    model = load_RF_File()
    return model.prediction(emotions)[0]
