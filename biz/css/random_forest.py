import pandas as pd
import pickle

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def build_Random_Forest():
    rfdf = pd.read_csv(facial_expression_data_path)
    target_column = rfdf['satisfaction']
    xTrain, xTest, yTrain, yTest = train_test_split(rfdf, target_column, test_size = 0.5, stratify=rfdf['satisfaction'], random_state=123456)
    irs_rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=123456)
    irs_rf.fit(xTrain, yTrain)

    return irs_rf

def RF_To_File(model):
    RF_pkl = open(RF_Pickle_Path, 'wb')
    pickle.dump(model, RF_pkl)
    RF_pkl.close()
    return

def load_RF_File():
    RF_pkl = open(RF_Pickle_Path, 'rb')
    return pickle.load(RF_pkl)