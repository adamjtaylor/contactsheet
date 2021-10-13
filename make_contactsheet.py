
import argparse
from tifffile import TiffFile
from matplotlib.image import imsave
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
from skimage.util import montage
import numpy as np
import sys
import os


parser = argparse.ArgumentParser(description = 'Create a contact sheet of scenes and channels from a tiff')
parser.add_argument(
    'input',
    type=str,
    help='the input file (openable by tifffile)'
    )
parser.add_argument(
    '--output',
    dest = "output",
    type = str,
    default = "contactsheet.png",
    help='the output file name'
    )
parser.add_argument('--dpi',
    dest = "dpi",
    type=int,
    default = 600,
    help='the output dpi'
    )

args = parser.parse_args()

def pull_series(path, level):
    with TiffFile(path) as tif:
        images = []
        for series in tif.series:
            i = series.levels[-1].asarray()
            images.append(i)
    return images

def plot_fig(image):
    channel_index = np.argmin(image.shape)  
    if image.shape[channel_index] == 3:
        fig = imshow(image)
        fig.axis('off')
    else: 
        image_rearrange = np.moveaxis(image, channel_index, 0)
        image_montage = montage(image_rearrange,  rescale_intensity=True)
        fig = imshow(image_montage, cmap = 'gray')
        fig.axis('off')

    return fig

def arrange_figs(images):
    figs, axs = plt.subplots(len(images))
    for index, image in enumerate(images):
        axs[index].imshow(image)
        axs[index].axis('off')
    return figs


def main():

    images = pull_series(args.input, -1)
    figs = list(map(plot_fig, images))

    fig = arrange_figs(figs)

    fig

    plt.savefig(args.output, dpi = args.dpi, bbox_inches='tight')

if __name__ == "__main__":
    main()  