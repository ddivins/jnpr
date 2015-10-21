# David Divins PyEZ
# ddivins@juniper.net
# 10-20-2015

import code
import datetime
import json
import logging
import numpy as np
import os.path
import sys
import yaml
from lxml import etree
from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.factory import loadyaml
from jnpr.junos.utils.sw import SW
from jnpr.junos.exception import ConnectError

#Setup Variables
csv = 'csv/csv.csv'
userName = 'juniper'
userPassword = 'jnpr123'

#package = '/var/tmp/junos-vsrx-12.1X46-D35.1-domestic.tgz'
package = 'code/junos-vsrx-12.1X46-D35.1-domestic.tgz'
remote_path = '/var/tmp'
validate = True
#noCopy tells script whether to scp code
#True means code is already on device
#False means Copy Code
noCopy = True

#Create 2D Array from csv [name,ip]
devList=np.genfromtxt(csv,delimiter=',',dtype=None)

#Setup Views (Optional)
#mydefs = loadyaml('yaml/myView.yml')
#globals().update(mydefs)

def myprogress(dev, report):
  print "host: %s, report: %s" % (dev.hostname, report)

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
			dev.timeout = 900

        	except Exception as err:                               
                	sys.stderr.write('Cannot connect to device: {0}\n'.format(err))

		#Do RPC/Work
		try:
			#Start Work here

			#Create an instance of SW
			sw = SW(dev)

			try:
				ok = sw.install(package=package, remote_path=remote_path, progress=myprogress, validate=validate, no_copy=noCopy, timeout=1800)
		
			except Exception as err:
				msg = 'Unable to install software, {0}'.format(err)
				print(msg)
				ok = False
		
			if ok is True:
				print('Software installation complete. Rebooting')
				rsp = sw.reboot()
				print('Upgrade pending reboot cycle, please be patient.')
				print(rsp)
			else:
				msg = 'Unable to install software, {0}'.format(ok)
				print(msg)
	
			#Write Element Seperator	
			print("+++++++++++++++++++++++++++++++++++++++++++++++++")
		
			#Close Device
			dev.close()

        	except Exception as err:
                	sys.stderr.write('Cannot perform RPC on device: ' + row[1] + '\n'.format(err))
                	print("+++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == "__main__":
	main()
