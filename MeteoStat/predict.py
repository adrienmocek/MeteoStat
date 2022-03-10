import os
from math import sqrt
from tkinter import Y
from webbrowser import get
from tensorflow.keras import models
import joblib
import pandas as pd
from google.cloud import storage
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

PATH_TO_LOCAL_MODEL = 'model.joblib'



def get_model():

    """
    load weights from the trained model
    """
    return models.load_model("MeteoStat/data/AJ_my_model_mse")

def predict(X):

    """
    input X : ndarray of size (10,650,420) representing a set of 10 images

    returns y_pred as ndarray of size (10,130,84) representing a set of 10 images
    """

    model = get_model()

    y_pred = model.predict(X)

    # - 2 dimensions
    y_pred = np.squeeze(y_pred, axis = 0)
    y_pred = np.squeeze(y_pred, axis = 3)

    return y_pred


if __name__ == '__main__':
    print(predict())
