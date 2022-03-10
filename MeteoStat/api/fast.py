
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import datetime as dt
from MeteoStat.data import open_data, scrapping_images
from MeteoStat.preprocessing import preproc_data
from MeteoStat.data import save_data
from MeteoStat.predict import predict
import numpy as np
from MeteoStat.predict import get_model
import matplotlib.image as mpimg
#rom visualization import superpose_image
from MeteoStat.visualization import make_gif
from fastapi.responses import  FileResponse


app = FastAPI()
carte_test = mpimg.imread("images/carte_test.png")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict", response_class=FileResponse)
def make_prediction(date):
    """
    input start date as a string
    returns 20 images (10 true, 10 pred)
    """
    #transform string into start date
    start = dt.datetime.strptime(date,'%Y-%m-%d_%H%M')
    finish = start + dt.timedelta(minutes=150)
    #save 10 images from start to finish as png in image_preproc folder
    saved_images = scrapping_images(start, finish)
    imgs = []
    preproc_images = []
    for date_save in saved_images:
        imgs.append(open_data(date_save))

    #transform them into preprocessed X images
    for img in imgs:
        preproc_images.append(preproc_data(img))

    X = np.array([x[0] for x in preproc_images])
    X = X[:, ::5, ::5]
    X = np.expand_dims(X, axis=3)
    X = np.expand_dims(X, axis=0)
    print(X.shape)
    y_pred = predict(X)

    X = np.squeeze(X, axis = 0)
    X = np.squeeze(X, axis = 3)

    y_pred = (255 * y_pred).astype(int)
    y_final = X + y_pred
    print(y_pred.shape)
    print(len(y_final))
    make_gif(y_final, "prediction.gif")

    return FileResponse("prediction.gif")
    #return y_pred

if __name__ == '__main__':
    print(make_prediction('2021-07-12_0945'))
