from tifffile import TiffFile
from matplotlib.image import imsave
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
from skimage.util import montage
import numpy as np
import sys
import os


def pull_series(path, level):
    with TiffFile(path) as tif:
        images = []
        for series in tif.series:
            i = series.levels[-1].asarray()
            images.append(i)
    return images

def plot_rgb(images):
    fig, axs = plt.subplots(len(images))
    for index, image in enumerate(images):
        channel_index = np.argmin(image.shape)  
        if channel_index == 3:
            axs[index].imshow(image)
            axs[index].axis('off')
        else: 
            image_rearrange = np.moveaxis(image, channel_index, 0)
            image_montage = montage(image_rearrange,  rescale_intensity=True)
            axs[index].imshow(image_montage, cmap = 'gray')
            axs[index].axis('off')

    return(fig)

def main():
    path = sys.argv[1]
    output = 'contactsheet.png'

    images = pull_series(path, -1)
    fig  = plot_rgb(images)

    fig

    plt.savefig(output, dpi = 300, bbox_inches='tight')

if __name__ == "__main__":
    main()  