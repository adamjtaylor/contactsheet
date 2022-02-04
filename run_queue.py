#!/usr/bin/python

import csv
import os
import sys
import argparse
import time
from urllib.parse import urlunsplit, urlencode, urlparse
import re
import synapseclient
import pandas as pd
import boto3
syn = synapseclient.Synapse()
syn.login()

parser = argparse.ArgumentParser(description = 'Pull image tags from an streaming s3 object')
parser.add_argument('queue',
                    type=str,
                    help='name of a csv with a uri or synapse id per row')
parser.add_argument('--type',
                    type=str,
                    choices=['uri', 'synid'],
                    help='what the list contains: one of "uri" or "synid"')
parser.add_argument('--aws_profile',
                    type=str,
                    default='sandbox-developer',
                    help='aws profile to use')
parser.add_argument('--gs_profile',
                    type=str,
                    default='htan-dcc-gcs',
                    help='gs profile to use')

args = parser.parse_args()


def get_cloud_uri(synid):
    entity = syn.get(entity = synid, downloadFile = False)
    key = entity._file_handle['key']
    bucketName = entity._file_handle['bucketName']
    concreteType = entity._file_handle['concreteType']
    if re.search(r'GoogleCloudFileHandle', concreteType):
        scheme = "gs"
    elif re.search(r'S3FileHandle', concreteType):
        scheme = "s3"
    cloud_uri = urlunsplit((scheme,bucketName,key, '', ''))
    return cloud_uri


with open(args.queue, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    count = sum(1 for _ in datareader)
    csvfile.seek(0)
    datareader = csv.reader(csvfile)
    n = 1
    for row in datareader:
        if args.type == "uri":
            uri = row[0]
            output = uri
        elif args.type == "synid":
                try:
                    uri = get_cloud_uri(row[0])
                except:
                    n = n+1
                    continue
                output = row[0]
                print(output + ": " + uri)
        parsed_uri = urlparse(uri)
        scheme = parsed_uri.scheme
        if scheme == "s3":
            profile = args.aws_profile
        elif scheme == "gs":
            profile = args.gs_profile
        print(f'Processing file {str(n)} of {str(count)}: {row[0]}')
        os.system('python contactsheet-stream.py "' + uri + '" --profile ' + profile + ' --output ' + output)
        print("File " +str(n) + " complete")
        print("")
        print("")
        n = n+1

now = str( int( time.time() ) )

#newname = args.queue.replace("queue", "queue/complete") + "_" + now + ".csv"

#os.rename(args.queue, str(newname))
        
