import requests
from io import BytesIO
from datetime import date, timedelta, datetime
from PIL import Image, UnidentifiedImageError
import pandas as pd
import matplotlib.image as mpimg


def iteration_15min(start, finish):
    ## Generateur de (an, mois, jour, heure, minute)
     while finish > start:
        start = start + timedelta(minutes=15)
        yield (start.strftime("%Y"),
               start.strftime("%m"),
               start.strftime("%d"),
               start.strftime("%H"),
               start.strftime("%M")
               )


def scrapping_images (start, finish) :
    """Scrape images radar en ligne toutes les 15 min
    entre deux dates donnees sous forme de datetime.datetime
    Sauvegarde les dates pour lesquelles la page n'existe pas.  """
    missing_times = []
    for (an, mois, jour, heure, minute) in iteration_15min(start, finish):
        ## url scrapping :
        url = (f"https://static.infoclimat.net/cartes/compo/{an}/{mois}/{jour}"
            f"/color_{jour}{heure}{minute}.jpg")
        date_save = f'{an}_{mois}_{jour}_{heure}h{minute}'

        try :
            open_save_data(url, date_save)

        except UnidentifiedImageError :
            print (date_save, ' --> Missing data')
            missing_times.append(date_save)
    ## Save missing data list :
    missing_data_name = f'missing_datetimes_{start.strftime("%Y")}\
        {start.strftime("%m")}{start.strftime("%d")}_to_{finish.strftime("%Y")}\
            {finish.strftime("%m")}{finish.strftime("%d")}'
    pd.DataFrame(missing_times).to_pickle(missing_data_name)
    print(missing_times)



def open_save_data(url, date_save):
    ## Ouvre l'image pointee par url
    ## Enregistre l'image avec l'extention date_save

    print(url, date_save)

    response = requests.get(url)

    img = Image.open(BytesIO(response.content))
    img.save( f"images/radar{date_save}.png")
    pass

def open_data(date_save):
    print('Open '+date_save)
    img = mpimg.imread(f"images/radar{date_save}.png")
    return img

def save_data(img, date_save):

    ## Save as image :
    print('save image')
    img = Image.fromarray((img * 255).astype(np.uint8))
    img.save( f"images_preproc/radar_preproc{date_save}.png")
    pass

if __name__ == '__main__' :

    start = datetime(2018, 10, 2, 12)
    finish = datetime(2018, 10, 2, 14, 30)

    scrapping_images (start, finish)
