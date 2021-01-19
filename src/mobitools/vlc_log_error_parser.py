'''
Created on Oct 4, 2019

@author: rliu01
'''
from time import sleep
'''
Created on Sep 25, 2019

@author: rliu01
'''
import re
import os
import ConfigParser
import subprocess
import vlc
import sys

# log_file_path = r"d:\vlc.txt"
# 
# pattern1 = '(error)'
# pattern2 = '(warning)'
# read_line = False
# with open(log_file_path,"r") as file:
#     match_list = []
#     for line in file:
# #         print line
#         if read_line == True:
#             match_list.append(line)
#             if re.match(pattern2, line, re.S):
#                 read_line = False
#         else:
#             if re.match(pattern1, line, re.S):
#                 match_list.append(line)
#                 read_line = True
# file.close()
#                 
# print '\n'.join(map(str,match_list))

config_file_path = r"d:\vlc_parser.conf.txt"
config = ConfigParser.RawConfigParser()
config.read(config_file_path)
# vlc_exe_path = config.get('path','vlc_path')
vlc_log_path = config.get('path','log_path')
vlc_filtered_error_path = config.get('path','filtered_error_path')
record_path = config.get('path', 'record_path')
channel_url = {}
for (k,v) in config.items('url'):
    channel_url[k] = v
outfile = os.path.join(record_path, '2052_dash')
print outfile
cmd1 = "sout=file/ts:%s" % outfile
Instance = vlc.Instance('--verbose 3')
player = Instance.media_player_new()
# print channel_url.get('2052_dash')
# Media = Instance.media_player_new()
player.set_mrl(channel_url.get('2052_dash'),cmd1)
# player.set_media(Media)
player.play()
sleep(60*30)
player.stop()
Instance.log_unset()
