'''
Created on Mar 4, 2019

@author: rliu01
'''
import streamlink

if __name__ == '__main__':
    url = "http://mobitvps0.centralus.cloudapp.azure.com:8080/mm/dash/live/2043/LIVESERVICE_1234/segtimeline=true,group=TG_DAI_FULL_HD.mpd?StreamType=LIVE&vdalgov=timeline&DeviceId=RanTest&channelid=244460&icignorebreaks=1"
    streams = streamlink.streams(url)
    fd = streams.open()
    data = fd.read(1024)
    print data
    fd.close()