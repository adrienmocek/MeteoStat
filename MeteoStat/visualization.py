import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def show_image(array):
    """
    array: image to be displayed, np.array with 1 channel or 3 channels
    """
    fig = plt.figure(figsize=(12,12))
    plt.imshow(array)
    plt.axis('off')
    return fig

def show_images(arrays: list, nrows: int=1, ncols: int=2) -> None:
    """
    arrays: list of images
    """
    fig, axs = plt.subplots(nrows, ncols, figsize=(12,12))
    for ax, array in zip(axs.flat, arrays):
        ax.imshow(array)
        ax.axis('off')
    fig.tight_layout()

def save_figure(fig, fname):
    fig.savefig(fname)

def make_mask(rain, norain, tolneg, tolpos):
    """
    rain: image with clouds
    norain: background
    tolneg and tolpos: tolerance
    for each pixel, returns 0 if pixelwise difference is between -tolneg and +tolpos and 1 otherwise
    """
    mask = (((rain-norain) < (- tolneg)) | ((rain-norain) > tolpos )).any(axis=2).astype(int)
    mask = np.expand_dims(mask, axis=2)
    return mask


def make_extract(rain, norain, tolneg, tolpos):
    mask = make_mask(rain, norain, tolneg, tolpos)
    return mask * rain

def superpose_image(background, img1, img2):
    """
    background: background image, np.array with 3 channels (RGB)
    img1: grayscale image, to be displayed in red
    img2: grayscale image, to be displayed in green
    """
    plt.figure(figsize=(12,12))
    plt.imshow(background + img1 * (1,69/255,0) + img2 * (0, 0, 1))
    plt.axis('off')

def make_gif(frames,f_name,):
    frames=[Image.fromarray(np.uint8(frame)) for frame in frames]
    frame_one = frames[0]
    frame_one.save(f_name, format="GIF", append_images=frames,
               save_all=True, duration=5, loop=0)

def crop_image(img, x1, x2, y1, y2):
    return img[x1:x2, y1:y2, :]
