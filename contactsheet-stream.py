
import argparse
from tifffile import TiffFile
from matplotlib.image import imsave
from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt
from skimage.util import montage
import numpy as np
from urllib.parse import urlparse

import zarr
import sys
import os
import io
import boto3
import re


parser = argparse.ArgumentParser(description = 'Create a contact sheet of scenes and channels from a tiff')
parser.add_argument('--dpi',
    dest = "dpi",
    type=int,
    default = 600,
    help='the output dpi'
    )
parser.add_argument('--level',
    dest = "level",
    type=int,
    default = -1,
    help='the image pyramid level to extract'
    )
parser.add_argument('uri',
                    type=str,
                    help='name of a s3 bucket that your profile has access to')
parser.add_argument('--profile',
                    type=str,
                    help='aws profile to use')
parser.add_argument('--output',
                    type=str,
                    help='to parse for output filenames')

args = parser.parse_args()

# Define a streaming s3 object file class S3File(io.RawIOBase):
class S3File(io.RawIOBase):
    """
    https://alexwlchan.net/2019/02/working-with-large-s3-objects/
    """
    def __init__(self, s3_object):
        self.s3_object = s3_object
        self.position = 0

    def __repr__(self):
        return "<%s s3_object=%r>" % (type(self).__name__, self.s3_object)

    @property
    def size(self):
        return self.s3_object.content_length

    def tell(self):
        return self.position

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            self.position = offset
        elif whence == io.SEEK_CUR:
            self.position += offset
        elif whence == io.SEEK_END:
            self.position = self.size + offset
        else:
            raise ValueError("invalid whence (%r, should be %d, %d, %d)" % (
                whence, io.SEEK_SET, io.SEEK_CUR, io.SEEK_END
            ))

        return self.position

    def seekable(self):
        return True

    def read(self, size=-1):
        if size == -1:
            # Read to the end of the file
            range_header = "bytes=%d-" % self.position
            self.seek(offset=0, whence=io.SEEK_END)
        else:
            new_position = self.position + size

            # If we're going to read beyond the end of the object, return
            # the entire object.
            if new_position >= self.size:
                return self.read()

            range_header = "bytes=%d-%d" % (self.position, new_position - 1)
            self.seek(offset=size, whence=io.SEEK_CUR)

        return self.s3_object.get(Range=range_header)["Body"].read()

    def readable(self):
        return True



def pull_series(path, level):
    with TiffFile(path) as tif:
        images = []
        for series in tif.series:
            i = series.levels[-1]
            z = zarr.open(i.aszarr())
            images.append(z)
    return images


def plot_fig(image):
    channel_index = np.argmin(image.shape)  
    if image.shape[channel_index] == 3:
        return image
    else: 
        image_rearrange = np.moveaxis(image, channel_index, 0)
        image_montage = montage(image_rearrange, rescale_intensity=True)
        return image_montage

def arrange_figs(images):
    figs, axs = plt.subplots(len(images))
    for index, image in enumerate(images):
        axs[index].imshow(image)
        axs[index].axis('off')
    return figs


def main():
    # Stream the highest level image
    print("Parsing URI: " + args.uri)
    o = urlparse(args.uri, allow_fragments=False)
    provider = o.scheme
    print("Provider: " + provider)
    bucket = o.netloc
    print("Bucket: " + bucket)
    key = o.path.lstrip('/')
    print("Key: " + key)


    print("Loading image")

    if provider == "s3":
      session = boto3.session.Session(profile_name=args.profile)
      s3 = session.client('s3')
      s3_resource = session.resource('s3')

    if provider == "gs":
      print("Accessing GCS resource")
      session = boto3.session.Session(profile_name=args.profile)
      s3_resource = session.resource('s3',endpoint_url = "https://storage.googleapis.com")

    print("Getting object")
    s3_obj = s3_resource.Object(bucket_name=bucket, key=key)
    print("Creating streaming s3 file")
    s3_file = S3File(s3_obj)
    
    
    images = pull_series(s3_file, args.level)
    figs = list(map(plot_fig, images))

    if len(figs) > 1:
        fig = arrange_figs(figs)
    else:
        fig = imshow(figs[0])
        plt.axis('off')
        

    fig

    if re.match(r'syn\d{8}', args.output):
        output_path = "outputs/" + bucket + "/" + args.output + ".png"
    else:
        #basename = os.path.basename(key)
        basename = Path(key)
        extensions = "".join(basename.suffixes)
        output_path =str(basename).replace(extensions, ".json")
        output_path = "outputs/" + bucket + "/" + output_path

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path, dpi = args.dpi, bbox_inches='tight')

if __name__ == "__main__":
    main()  