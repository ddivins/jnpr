# jnpr
JunOS PyEZ

##configs  
Directory containing config snippets  
Sample "config.set" is provided  

##csv  
Directory contains your host file to iterate over  
Format is "host,ip"  
Please have at least 2 rows  
sample "csv.csv" is provided  

##output
Default directory for output of scripts

##templates  
Directory contains templates to create new scripts  

##yaml  
Directory contains your custom yaml files  
Custom version of PhyPortErrorStats provided  

##configDevice.py  
Script to push identical code bits to all devices  
Code snippet is in seperate file in config directory  
NOTE: Not a ton of error checking (yet)  

##getLogs.py  
Script to tgz the "/var/logs" directory and then scp the files over  
 
##getRSI.py  
Script to get "request support information" into individual files  
Caution, script takes time  

##getStats.py
Script to pull interface statistics from all interfaces. Right now, it pulls bps and pps.

##nrfuCheck.py  
Script to run a customer's Network Ready For Use Test (NRFU)  
Checks for Input/Output errors  
Runs a number of show commands  

##pushCode.py  
Script to scp JunOS code to a device   
Does not install software, simple transfers and does md5  
Companion script is upgradeDevice.py  

##upgradeDevice.py  
Script to upgrade JunOS  
Code can be staged (via pushCode.py or other means)  
This script can upload code as well, however, it will upgrade and reboot devices  
