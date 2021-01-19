#!/usr/bin/python

import sys, getopt
import shutil
import ConfigParser
import os

abrain_config_file = '/opt/rgb/etc/abrain.config'
abrain_config_file_orig = '/opt/rgb/etc/abrain.config.orig'
prrs_config_file = "/opt/rgb/etc/prrs.config"
prrs_config_file_orig = '/opt/rgb/etc/prrs.config.orig'

class mobitv_config():
    def __init__(self):
        self.abrain_path = abrain_config_file
        self.abrain_path_orig = abrain_config_file_orig
        self.prrs_path = prrs_config_file
        self.prrs_path_orig = prrs_config_file_orig
    def updateabrain(self):
        if not os.path.isfile(self.abrain_path_orig) : 
            shutil.copy2(self.abrain_path, self.abrain_path_orig)
        c = ConfigParser.RawConfigParser()
        c.read(self.abrain_path)
#         print(c.sections())
        if not c.has_section('Customer') :
            c.add_section('Customer')
        c.set('Customer', 'type', 'mobitv')
        c.set('HLS', 'break_event_signal_type', 'text')
        c.set('System', 'mongo_db_url', 'mongodb://10.0.0.26:27017')
        c.set('ClusterPlugin', 'prrs_knownmembers', '10.0.0.29,10.0.0.37,10.0.0.20')
        abrain_config = open(self.abrain_path, 'w')
        c.write(abrain_config)
        abrain_config.close()
    def updateprrs(self):
        if not os.path.isfile(self.prrs_path_orig) : 
            shutil.copy2(self.prrs_path, self.prrs_path_orig)
        c = ConfigParser.RawConfigParser()
        c.read(self.prrs_path)
#         print(c.sections())
        c.set('WebService', 'threads', '44')
        c.set('System', 'cluster_plugin_mode', '1')
        c.set('System', 'log_forwarder', '10.0.0.78:12345')
        c.set('System', 'profile_matching_algorithm', '2')
        c.set('System', 'drift_tracking', 'False')
        c.set('ADS', 'ads_psn_mode', 'psn_tagging')
        c.set('ADS', 'ads_break_tolerance', '1000')
        c.set('ADS', 'ads_routing_param', 'adsroute')
        c.set('ADS', 'manifest_targeting_parameters', 'BI_Targets')
        c.set('ADS', 'build_manifest_using_prefix', 'True')
        c.set('ADS', 'ad_client_beacon_base_url', 'http://10.0.0.26:8123/img_rvast_beacon')
        prrs_config = open(self.prrs_path, 'w')
        c.write(prrs_config)
        prrs_config.close()



def main(argv):
    customer_type = ''
    node_type = ''
    try:
        opts, args = getopt.getopt(argv,"hc:n:",["ctype=","ntype="])
    except getopt.GetoptError:
        print 'custom_type.py -c <customer_type> -n <node_type>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'custom_type.py -c <customer_type> -n <node_type>'
            sys.exit()
        elif opt in ("-c", "--ctype"):
            customer_type = arg
        elif opt in ("-n", "--ntype"):
            node_type = arg
    if customer_type == 'mobitv':
        new_node = mobitv_config()
        print 'customer type is ', customer_type
        print 'node type is ', node_type
        if node_type is 'awe' or 'prrs' :
            print 'updating abring.config', node_type
            new_node.updateabrain()
            print "abrain.config updated\n Warning: prrs_knownmembers should be updated manually!"
        if node_type == 'prrs':
            print 'updating prrs.config'
            new_node.updateprrs()
            print "prrs.config updated\n Warning: AdWorkflow Section Should Be Updated Manually\n Warning: parameter log_forwarder and ads_parameter_map must be updated manually"
if __name__ == "__main__":
    main(sys.argv[1:])
    
