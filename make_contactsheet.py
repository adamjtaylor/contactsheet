from matplotlib import image
from tifffile import TiffFile
from matplotlib.image import imsave
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from skimage.util import montage
import sys
import os


def pull_series(path, level):
    with TiffFile(svs_path) as tif:
        images = []
        for series in tif.series:
            i = series.levels[-1].asarray()
            images.append(i)
    return images

def plot_rgb(images):
    fig, axs = plt.subplots(len(images))
    for index, image in enumerate(images):
        channel_index = np.argmin(images[0].shape)  
        if channel_index == 3:
            axs[index].imshow(image)
            axs[index].axis('off')
        else: 
            image_rearrange = np.moveaxis(image, channel_index, 0)
            montage = montage(image_rearrange,  rescale_intensity=True)
            axs[index].imshow(montage, cmap = 'gray')
            axs[index].axis('off')

    return(fig)

def main():
    path = sys.argv[1]
    output = 'contactsheet.png'

    images = pull_series(path, -1)
    fig  = plot_rgb(images)

    imsave(fig, output)

if __name__ == "__main__":
    main()  