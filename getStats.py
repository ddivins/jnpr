from pprint import pprint
from jnpr.junos import Device
from lxml import etree
from jnpr.junos.op.ethport import EthPortTable 
from jnpr.junos.op.phyport import PhyPortStatsTable
from jnpr.junos.op.phyport import PhyPortErrorTable
from jnpr.junos.factory.factory_loader import FactoryLoader
from jnpr.junos.factory import loadyaml
import code
import sys
import yaml
import json
import datetime
import numpy as np
import os.path

#Setup Variables
csv = 'csv/csv.csv'
userName = 'juniper'
userPassword = 'jnpr123'
save_path = 'output'
#save file name prefix
prefix = 'dev'

#Create 2D Array from csv [name,ip]
devList=np.genfromtxt(csv,delimiter=',',dtype=None)

#Setup Views
mydefs = loadyaml('yaml/allport.yml')
globals().update(mydefs)

def main():
	#Setup for output
	now = datetime.datetime.now()
	txt = os.path.join(save_path, "stats-" + prefix + "-" + now.strftime("%Y%m%d-%H%M") + ".txt")
	text_file =  open(txt, "w")
	text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++")
	text_file.write('\n')

	#iterate over csv
	for row in devList:

        	#define host for pyez
        	dev = Device(host=row[1], user=userName, password=userPassword)
        	try:

                	#Status
                	now1 = datetime.datetime.now()
                	pprint("NRFU Check on " + row[0] + " | " + row[1] + " at " + now1.strftime("%Y-%m-%d %H:%M"))

			dev.open()
			dev.timeout = 300
			phyErrorTable = MyPhyPortErrorTable(dev).get()

        	except Exception as err:                               
                	sys.stderr.write('Cannot connect to device: {0}\n'.format(err))
                	text_file.write('Cannot connect to device: {0}\n'.format(err) + '\n')
			text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++")		
			text_file.write('\n')

		#Do RPC
		try:

			#Write Hostname and Version
			print("Hostname and Version")
			text_file.write(dev.facts['hostname'] + '\n')
			text_file.write(dev.facts['version'] + '\n')
			text_file.write('\n')

			#Get phyPortErrorTable Info
			print ("show interfaces | match pps ")
			text_file.write("show interfaces | match pps" + '\n')

			for intf in phyErrorTable:
				text_file.write(intf.name + '\n')
				text_file.write('{} : {}'.format("Input bps",intf.rx_bps) + '\n')
				text_file.write('{} : {}'.format("Input pps",intf.rx_pps) + '\n')
				text_file.write('{} : {}'.format("Output bps",intf.tx_bps) + '\n')
				text_file.write('{} : {}'.format("Output pps",intf.tx_pps) + '\n')
			text_file.write('\n')

			#Do RPC Show Commands

			print("+++++++++++++++++++++++++++++++++++++++++++++++++")
			text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++")
			text_file.write('\n')
		
			#Close Device
			dev.close()

        	except Exception as err:
			sys.stderr.write('Cannot perform RPC on device: {0}\n'.format(err))
                	text_file.write('Cannot perfoen RPC on device: {0}\n'.format(err) + '\n')
                	text_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++")
                	text_file.write('\n')

if __name__ == "__main__":
	main()
