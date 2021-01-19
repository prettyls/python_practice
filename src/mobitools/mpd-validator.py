#
# mpd-validator.py
#

import urllib2
import re
from urlparse import urlparse, parse_qs
import os
import datetime
import time
import logging
import urllib
import xml.etree.ElementTree as ET
from collections import OrderedDict

G_MEDIA_SEQUENCE_TAG = '#EXT-X-MEDIA-SEQUENCE:'
G_DISCONTINUITY_SEQUENCE_TAG = '#EXT-X-DISCONTINUITY-SEQUENCE:'
G_DISCONTINUITY_TAG = '#EXT-X-DISCONTINUITY'


class Mpd:
    
    mpdString = ''  # The full XML string for the MPD

    minBufferTime = 0    # "PT2S" 
    mpdType = 'dynamic'  # (live stream)
    timeShiftBufferDepth = 0      #"PT9M"    (window size)
    minimumUpdatePeriod = 0      #"PT9S"     (mpd polling interval - decode this and use as the polling delay interval)
    availabilityStartTime = ''   #"1970-01-01T00:00:22Z"
    suggestedPresentationDelay = 0 #"PT12S"   (suggested distance from live edge?)
    id = ''  #"2052"  (mobi channel)
    publishTime = ''  #"2019-09-28T02:02:22Z" (when this mpd was created)


    # Map period id to period object
    periods = {}

    def __init__(self, paramMpdString):

        self.mpdString = paramMpdString

        self.minBufferTime = 0    # "PT2S" 
        self.mpdType = 'dynamic'  # (live stream)
        self.timeShiftBufferDepth = 0      #"PT9M"    (window size)
        self.minimumUpdatePeriod = 0      #"PT9S"     (mpd polling interval - decode this and use as the polling delay interval)
        self.availabilityStartTime = ''   #"1970-01-01T00:00:22Z"
        self.suggestedPresentationDelay = 0 #"PT12S"   (suggested distance from live edge?)
        self.id = ''  #"2052"  (mobi channel)
        self.publishTime = ''  #"2019-09-28T02:02:22Z" (when this mpd was created)

        self.periods = {}


class Period:

    id = ''
    start = ''
    img_id = ''
    base_url = ''

    def __init__(self, paramId, paramStart, paramImgId, paramBaseUrl):
        self.id = paramId
        self.start = paramStart
        self.img_id = paramImgId
        self.baseUrl = paramBaseUrl



def writeToFile (mpdString, sequenceNumber):

        ext = 'mpd'

        filename = 'mpd-' + str(sequenceNumber).zfill(6) + '.' + ext

        path = os.path.join(os.path.curdir, 'mpd-sequence')

        if not os.path.exists(path):
            os.makedirs(path)

        filenamePath = os.path.join (path, filename)

        logging.info ('Writing ' + filenamePath)

        with open(filenamePath, 'w') as f:
                f.write(mpdString)


def logErrorMessage (errorMessage):
    print (errorMessage + '\n')
    logging.error (errorMessage)


def logInfoMessage (infoMessage):
    print (infoMessage + '\n')
    logging.info (infoMessage)


def readFromFile (filename):

    mpdString = ''

    with open(filename, 'r') as file:
        mpdString = file.read()

    return mpdString


def readFromHttp (url):

        mpdString = ''

        req = urllib2.Request(url)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                logging.error('download: connection error.')
                logging.error('Reason: ' + str(e.reason))
            elif hasattr(e, 'code'):
                logging.error('download: request error.')
                logging.error('Error code: ' + str(e.code))
        else:
            # request was successful.
            mpdString = response.read()
            response.close()

        return mpdString


# mpdSource = url or file path
def getMpd (mpdSource):

    mpdString = ''

    if (mpdSource.startswith('http')):
        mpdString = readFromHttp(mpdSource)
    else:
        mpdString = readFromFile(mpdSource)
    
    # parse mpdString as xml and create an Mpd object
    mpdXmlRoot = ET.fromstring(mpdString)

    mpd = Mpd(mpdString)

    # now walk all the periods in the mpd, create period objects, and put in mpd period map

    for p in mpdXmlRoot.findall('{urn:mpeg:dash:schema:mpd:2011}Period'):
        id = p.get('id')
        img_id = p.get('{urn:img}id')
        start = p.get('start')
        baseUrl = p.find('{urn:mpeg:dash:schema:mpd:2011}BaseURL').text
        #print ('id=' + id + ' img:id=' + img_id + ' start=' + start)

        period = Period(id, start, img_id, baseUrl)

        mpd.periods[id] = period
        mpd.orderedPeriods = OrderedDict(sorted(mpd.periods.items(), key=lambda t: t[0]))

    return mpd



def validatePeriods (currentMpd, previousMpd):

    status = True

    for cp_id, cp in currentMpd.orderedPeriods.iteritems():
        if (cp_id in previousMpd.orderedPeriods):
            prev_p = previousMpd.orderedPeriods[cp.id]
            if ((cp.start != prev_p.start) or (cp.baseUrl != prev_p.baseUrl)):
                errmsg = '\n\nERROR: period id mismatch: current id=' + cp.id + ' img:id=' + cp.img_id + ' start=' + cp.start + ' baseUrl=' + cp.baseUrl + '\n'
                errmsg += '                         previous id=' + prev_p.id + ' img:id=' + prev_p.img_id + ' start=' + prev_p.start + ' baseUrl=' + prev_p.baseUrl + '\n'
                logErrorMessage(errmsg)
                status = False
                break
    
    return status


def runUnitTests ():

    previousFile = 'ps-mpd-1037.xml'
    currentFile = 'ps-mpd-1046.xml'

    previousMpd = getMpd (previousFile)
    currentMpd = getMpd (currentFile)

    result = validatePeriods (currentMpd, previousMpd)

    msg = 'test 1: previous=' + previousFile + ' current=' + currentFile
    
    # True is the expected result
    if (result):
        msg += ' - PASSED'
    else:
        msg += ' - FAILED'

    logging.info (msg)
    print (msg + '\n')


    previousFile = 'ps-mpd-1055.xml'
    currentFile = 'ps-mpd-1104.xml'

    previousMpd = getMpd (previousFile)
    currentMpd = getMpd (currentFile)

    result = validatePeriods (currentMpd, previousMpd)

    msg = 'test 2: previous=' + previousFile + ' current=' + currentFile
    
    # False is the expected result
    if (not result):
        msg += ' - PASSED'
    else:
        msg += ' - FAILED'

    logging.info (msg)
    print (msg + '\n')





FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='mpd-validator.log', level=logging.DEBUG, format=FORMAT)
logging.info('mpd-validator started.')


testUrl = 'http://10.0.0.8:7050/mm/dash/live/2052/LIVESERVICE_MM/segtimeline=true,ManifestT.mpd?StreamType=LIVE&vdalgov=timeline&DeviceId=mpd-val-191005-2&channelid=244460'

downloadFileNumber = 0
currentMpd = None
previousMpd = None

errorCount = 0

unitTestMode = False
if (unitTestMode):
    runUnitTests()
    quit()



# Run until manually stopped.
while (True):

    # Append this query parameter to allow searching for a specific MPD sequence number in the PS debug log.
    mpdUrl = testUrl + '&mpd-validator-' + str(downloadFileNumber).zfill(6)

    currentMpd = getMpd(mpdUrl)

    # If we are past the first manifest, verify the discontinuity sequence.
    if downloadFileNumber > 0:

        print ('Checking mpd period id, downloadFileNumber=' + str(downloadFileNumber) + ' errors=' + str(errorCount) + '\n')

        result = validatePeriods (currentMpd, previousMpd)

        if not result:
            errorCount += 1

    writeToFile (currentMpd.mpdString, downloadFileNumber)

    downloadFileNumber += 1

    previousMpd = currentMpd

    time.sleep (9)

    # end while


print ('test complete')

# end mpd-validator.py
