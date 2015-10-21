# jnpr
JunOS PyEZ

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

##getLogs.py  
Script to tgz the "/var/logs" directory and then scp the files over  
 
##getRSI.py  
Script to get "request support information" into individual files  
Caution, script takes time  

##pushCode.py  
Script to scp JunOS code to a device  
Does not install software, simple transfers and does md5  
Companion script is upgradeDevice.py  

##upgradeDevice.py  
Script to upgrade JunOS
Code can be staged (via pushCode.py or other means)  
This script can upload code as well, however, it will upgrade and reboot devices  
