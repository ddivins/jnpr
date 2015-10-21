# David Divins PyEZ
# ddivins@juniper.net
# 10-20-2015

import code
import datetime
import json
import numpy as np
import os.path
import sys
import yaml
from lxml import etree
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.factory import loadyaml
from jnpr.junos.utils.scp import SCP

#Setup Variables
csv = 'csv/csv.csv'
userName = 'juniper'
userPassword = 'jnpr123'
output = 'output'

#Create 2D Array from csv [name,ip]
devList=np.genfromtxt(csv,delimiter=',',dtype=None)

def main():
	#iterate over csv
	for row in devList:

        	#Make Device Connection
        	dev = Device(host=row[1], user=userName, password=userPassword)
		try:
       			#Print Opening Header for Status
			now1 = datetime.datetime.now()
			pprint("Work starts on " + row[0] + " | " + row[1] + " at " + now1.strftime("%Y-%m-%d %H:%M"))

			#Open Device with Custom Timer
			dev.open()
			dev.timeout = 300

        	except Exception as err:                               
                	sys.stderr.write('Cannot connect to device: {0}\n'.format(err))

		#Do RPC/Work
		try:
			#Start Work here

			rsp = dev.rpc.file_archive(destination='/var/tmp/logs', source='/var/log/*', compress=True)

                	with SCP(dev, progress=True) as scp1:
				scp1.get("/var/tmp/logs.tgz", local_path=output+"/"+row[0]+"-"+now1.strftime("%Y-%m-%d-%H%M")+"-logs.tgz")

			#Write Element Seperator	
			print("+++++++++++++++++++++++++++++++++++++++++++++++++")
		
			#Close Device
			dev.close()

        	except Exception as err:
                	sys.stderr.write('Cannot perform RPC on device: ' + row[1] + '\n'.format(err))
                	print("+++++++++++++++++++++++++++++++++++++++++++++++++")


if __name__ == "__main__":
	main()
