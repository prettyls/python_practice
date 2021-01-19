#!/usr/bin/env python

import os
import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
def main():
    parser = ArgumentParser()
    parser.add_argument("-d",dest="inputpath")
    parser.add_argument("-o",dest="outputpath")
    args = parser.parse_args()
    inputpath = args.inputpath
    outputpath = args.outputpath

def createHLSSegment(filepath,outdir):

    for filename in os.listdir(filepath):

        if (filename.endswith(".mp4")):
            try:
                os.system('ffmpeg -y -i filename -codec copy -bsf:v h264_mp4toannexb -map 0 -f segment -segment_time 6 -segment_format mpegts -segment_list "index.m3u8" -segment_list_type m3u8 "/outdir/segment-%d.ts"')
            except IOError:
                print('unable to find' + filename + 'from' + filepath)
        else:
            continue
if __name__ == '__main__':
    main()
    createHLSSegment(inputpath,outputpath)