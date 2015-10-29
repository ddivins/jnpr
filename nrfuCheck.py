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
	txt = os.path.join(save_path, "nrfu-" + prefix + "-" + now.strftime("%Y%m%d-%H%M") + ".txt")
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
			print ("show interface statistics | match errors")
			text_file.write("show interface statistics | match errors" + '\n')

			for intf in phyErrorTable:
				text_file.write(intf.name + '\n')
				text_file.write('{} : {}'.format("Input Errors",intf.rx_err_input) + '\n')
				text_file.write('{} : {}'.format("Input Drops",intf.rx_err_drops) + '\n')
				text_file.write('{} : {}'.format("Input Framing Errors",intf.rx_err_frame) + '\n')
				text_file.write('{} : {}'.format("Input Runts",intf.rx_err_runts) + '\n')
				#text_file.write('{} : {}'.format("Input L3-Incompletes",intf.rx_err_l3-incompletes) + '\n')
				#text_file.write('{} : {}'.format("Input L2-Channel Errors",intf.rx_err_l2-channel) + '\n')
				#text_file.write('{} : {}'.format("Input L2-Mismatch Timing",intf.rx_err_l2-mismatch) + '\n')
				text_file.write('{} : {}'.format("Input FIFO Errors",intf.rx_err_fifo) + '\n')
				text_file.write('{} : {}'.format("Input Resource Errors",intf.rx_err_resource) + '\n')
				text_file.write('{} : {}'.format("Output Errors",intf.tx_err_output) + '\n')
				#text_file.write('{} : {}'.format("Output Carrier Transitions",intf.tx_err_carrier-transitions) + '\n')
				text_file.write('{} : {}'.format("Output Collisions",intf.tx_err_collisions) + '\n')
				text_file.write('{} : {}'.format("Output Drops",intf.tx_err_drops) + '\n')
				text_file.write('{} : {}'.format("Output Aged-Packets",intf.tx_err_aged) + '\n')
				text_file.write('{} : {}'.format("Output MTU Errors",intf.tx_err_mtu) + '\n')
				#text_file.write('{} : {}'.format("Output HS-Link-CRC Errors",intf.tx_err_hs-crc) + '\n')
				text_file.write('{} : {}'.format("Output FIFO Errors",intf.tx_err_fifo) + '\n')
				text_file.write('{} : {}'.format("Output Resouce Errors",intf.tx_err_resource) + '\n')
			text_file.write('\n')

			#Do RPC Show Commands
			print("show bgp summary")
			text_file.write("show bgp summary" + '\n')
			bgp = dev.rpc.get_bgp_summary_information({'format':'text'})
			text_file.write(etree.tostring(bgp))
			text_file.write('\n')

			print("show isis adjancency")
			text_file.write("show isis adjancency")
			isis = dev.rpc.get_isis_adjacency_information({'format':'text'})
			text_file.write(etree.tostring(isis))
			text_file.write('\n')

			print("show system core-dumps")
			text_file.write("show system core-dumps" + '\n')
			dumps = dev.rpc.get_system_core_dumps()
			text_file.write(etree.tostring(dumps))
			text_file.write('\n')

			print("show system alarms")
			text_file.write("show system alarms" + '\n')
			alarms= dev.rpc.get_system_alarm_information({'format':'text'})
			text_file.write(etree.tostring(alarms))
			text_file.write('\n')

			print("show chassis environment")
			text_file.write("show chassis environment" + '\n')
			environment = dev.rpc.get_environment_information({'format':'text'})
			text_file.write(etree.tostring(environment))
		
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
