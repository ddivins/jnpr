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
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *

#Setup Variables
csv = 'csv/csv.csv'
userName = 'juniper'
userPassword = 'jnpr123'
conf_file = 'configs/conf.set'

#Create 2D Array from csv [name,ip]
devList=np.genfromtxt(csv,delimiter=',',dtype=None)

#Setup Views (Optional)
#mydefs = loadyaml('yaml/myView.yml')
#globals().update(mydefs)

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

			#Bind Device to Config
			dev.bind( cu=Config )
			
			#Lock the configuration, load configuration changes, and commit
			print "Locking the configuration"
			try:
				dev.cu.lock()
				print "Locked"
			except LockError:
				print "Error: Unable to lock configuration"
				dev.close()
				return
			
			#Load The Config
			print "Loading configuration changes"
			try:
				dev.cu.load(path=conf_file, merge=True)
				print "Loaded"
                	except Exception as err:
                        	sys.stderr.write(err.message)
			except ValueError as err:
				print err.message
			except Exception as err:
				if err.rsp.find('.//ok') is None:
					rpc_msg = err.rsp.findtext('.//error-message')
					print "Unable to load configuration changes: ", rpc_msg

				print "Unlocking the configuration"
				try:
			       		dev.cu.unlock()
				except UnlockError:
			        	print "Error: Unable to unlock configuration"
				dev.close()
				return

			#Commit the Config
			print "Committing the configuration"
			try:
				dev.cu.commit()
				print "Commited"
			except CommitError:
				print "Error: Unable to commit configuration"
				print "Unlocking the configuration"
				try:
					dev.cu.unlock()
				except UnlockError:
					print "Error: Unable to unlock configuration"
				dev.close()
				return
				
			#Unlock the config
			print "Unlocking the configuration"
			try:
				dev.cu.unlock()
			except UnlockError:
				print "Error: Unable to unlock configuration"			
			
			#Close Device
			dev.close()
        	except Exception as err:
                	sys.stderr.write('Cannot perform RPC on device: ' + row[1] + '\n'.format(err))
		#Write Element Seperator	
		print("+++++++++++++++++++++++++++++++++++++++++++++++++")


if __name__ == "__main__":
	main()
