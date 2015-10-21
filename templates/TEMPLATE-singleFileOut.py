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

#Setup Variables
csv = 'csv/csv.csv'
userName = 'juniper'
userPassword = 'jnpr123'
save_path = 'output'
filePrefix = 'myReport'

#Create 2D Array from csv [name,ip]
devList=np.genfromtxt(csv,delimiter=',',dtype=None)

#Setup Views (Optional)
#mydefs = loadyaml('yaml/myView.yml')
#globals().update(mydefs)


def main():

	#Setup for output
	now = datetime.datetime.now()
	txt = os.path.join(save_path, filePrefix + "-" + now.strftime("%Y%m%d-%H%M") + ".txt")
	text_file =  open(txt, "w")
	#Write Opening Seperator
	text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++" + '\n')

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
                	text_file.write('Cannot connect to device: {0}\n'.format(err) + '\n')

		#Do RPC/Work
		try:
			#Start Work here




			#Write Element Seperator	
			print("+++++++++++++++++++++++++++++++++++++++++++++++++")
			text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++" '\n')
		
			#Close Device
			dev.close()

        	except Exception as err:
                	sys.stderr.write('Cannot perform RPC on device: ' + row[1] + '\n'.format(err))
                	print("+++++++++++++++++++++++++++++++++++++++++++++++++")
                	text_file.write('Cannot perform RPC on device: ' + row[1] + '\n'.format(err) + '\n')
                	text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++" + '\n')

if __name__ == "__main__":
	main()
