#!/usr/bin/env python 
## This script is to be used after running setup.py, if you have not run setup.py go do that first. 

import os
import tdclient
import logging
import subprocess
from config import *

# configure logging level. 
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

################################
# Step 2.0 - Check all config values are filled out
################################

logging.info("\r\n\r\n***** Step 2.0 *******\r\n")
logging.info("Checking config values")

if mbed_cloud_api_key=="CHANGE THIS":
	logging.info("\r\n[USER INSTRUCTION]Please add your Pelion DMS API Key to config.py\r\n")
	logging.info("exiting script")
	raise SystemExit

if mbed_cloud_device_id=="CHANGE THIS":
	logging.info("\r\n[USER INSTRUCTION]Please add the Pelion Device ID to config.py\r\n")
	logging.info("exiting script")
	raise SystemExit

if td_apikey=="CHANGE THIS":
	logging.info("[USER INSTRUCTION]]Please add your Treasure Data API key to config.py")
	logging.info("exiting script")
	raise SystemExit

#Check that repo is downloaded
if not os.path.isdir(mbedos_repo_projectname):
	logging.info("Repo not found, please run setup.py")
	raise SystemExit


################################
# Step 2.1 - Check all config values are filled out
################################

logging.info("\r\n\r\n***** Step 2.1 *******\r\n")
logging.info("Grabing data from Treasure Data")
with tdclient.Client(td_apikey) as client:
    job = client.query(td_database, td_query)
    logging.info("Runnig TD query... Please wait for it to finish (<30sec)...")
    # sleep until job's finish
    job.wait()
    logging.info("Result is")
    for row in job.result():
        logging.info(row)


###############################
# Step 2.2 - Compute custom algorithm
###############################

# get the avg value
logging.info("\r\n\r\n***** Step 2.2 *******\r\n")
x = 0
for thing in job.result():
	x = thing
algo_value = x[0]
logging.info("algo_value computed as "+str(algo_value))

###############################
# Step 2.3 - Compile new binary with custom algorithm
###############################

logging.info("\r\n\r\n***** Step 2.3 *******\r\n")

logging.info("setting Pelion API Key to environment variable")
os.chdir(mbedos_repo_projectname) # change working directory to be inside mbedos repo
os.environ["CLOUD_SDK_API_KEY"]=mbed_cloud_api_key
check = subprocess.check_output(["mbed", "config", "CLOUD_SDK_API_KEY", mbed_cloud_api_key])

logging.info("Running compile")
logging.info("Adding #define "+algo_name+"="+str(algo_value)+"to the binary")
logging.info("Please wait while we compile the new binary (~5min)")
check=subprocess.check_output(["mbed", "compile", "--target", target,"--toolchain", "GCC_ARM","-D"+algo_name+"="+str(algo_value)])
logging.debug("[Mbed Compile]"+check)
logging.info("Binary Compiled Successfully")

################################
# Step 2.4 - Send compiled binary to device using Pelion Update
################################
logging.info("\r\n\r\n***** Step 2.4 *******\r\n")
# issue update
logging.info("Pelion Update - Sending binary to device with ID:"+mbed_cloud_device_id)
logging.info("You can verify this works by hooking up a serial terminal to the device and watching the update happen.")
check = subprocess.check_output(["mbed", "dm" ,"update", "device", "-D", mbed_cloud_device_id, "-m", target , "-vv"])
logging.debug("[mbed dm update]"+check)
logging.info("SUCCESS!! your device should now be running your code. Please check the serial output to verify")

