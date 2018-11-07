import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


RF_model_file = 'biz/css/RF_model.joblib'
emotion_training_set = 'emotion_training_set.csv'


def build_Random_Forest():
    rfdf = pd.read_csv(emotion_training_set)
    target_column = rfdf['satisfaction']
    del rfdf['satisfaction']
    xTrain, xTest, yTrain, yTest = train_test_split(rfdf,
                                                    target_column,
                                                    test_size=0.5,
                                                    stratify=target_column,
                                                    random_state=736251)
    irs_rf = RandomForestClassifier(n_estimators=100,
                                    oob_score=True,
                                    random_state=487368)
    irs_rf.fit(xTrain, yTrain)
    accuracy_score(yTest, irs_rf.predict(xTest))
    return irs_rf


def RF_To_File(model):
    joblib.dump(model, RF_model_file)


def load_RF_File():
    return joblib.load(RF_model_file)
