#!/usr/bin/env python 
import os, logging
import config

# configure logging level. 
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.info("Welcome to the E2E Demo, please follow the prompts printed on screen")
logging.info("You will need to fill in the Pelion DMS and Treasure Data API Keys in the script when prompted")

###############################
# Step 1.1 - Clone down and setup mbed-os-example code, and flash to the board
###############################
import subprocess,sys

logging.info("\r\n\r\n***** Step 1.1 *******\r\n")
logging.info("Cloning the mbed os example repo, make sure the board is plugged into the computer")
logging.debug("project name detected as "+mbedos_repo_projectname)

if mbed_cloud_api_key=="CHANGE THIS":
	logging.info("\r\n[USER INSTRUCTION]Please add your Pelion DMS API Key to config.py\r\n")
	logging.info("exiting script")
	raise SystemExit

#Check that the board is connected
check = subprocess.check_output(["mbedls","-p"])
if target not in check:
	logging.info(target+" not detected, please plug it into the computer")
else:
	logging.info(target+" detected")

#Check that repo is downloaded
if not os.path.isdir(mbedos_repo_projectname):
	logging.info("Repo not found, importing it now")
	check = subprocess.check_output(["mbed","import",mbedos_repo])
	logging.debug("[MBED IMPORT]"+check)

os.chdir(mbedos_repo_projectname) # change working directory to be inside mbedos repo

# set Mbed CLoud API key into the environment
logging.info("setting mbed cloud api key into the environment variables")
os.environ["CLOUD_SDK_API_KEY"]=mbed_cloud_api_key
check = subprocess.check_output(["mbed", "config", "CLOUD_SDK_API_KEY", mbed_cloud_api_key])

# check if update certs are in the project.
if not os.path.isdir(".update-certificates"):
	# If no update certs, add them (only first time)
	logging.info("No device certs found, adding now...")
	check = subprocess.check_output(["mbed", "dm", "init", "-a", mbed_cloud_api_key, "-d", "\"http://os.mbed.com\"", "--model-name", "\"modelname\"", "-q", "--force"])
	logging.debug("[Mbed Device Management]"+check)
	logging.info("\r\n[USER INSTRUCTION] Please modify "+mbedos_repo_projectname+"/mbed_app.json to include the wifi ssid / password and the Treasure Data API Key")
	raise SystemExit

# Compile and flash the program
logging.info("Please wait while we compile the new binary (This could take a while (5-10min)...)")
check=subprocess.check_output(["mbed", "compile", "--target", target,"--toolchain", "GCC_ARM","--flash"])
logging.debug("[Mbed Compile]"+check)
logging.info("Binary has been flashed to the board")

###############################
# Step 1.2 - Add the Pelion Device ID to config.py
###############################

logging.info("\r\n\r\n***** Step 1.2 *******\r\n")
logging.info("Add the device ID to config.py. Get it from portal.mbedcloud.com or from the serial terminal hooked up to the device")

if mbed_cloud_device_id=="CHANGE THIS":
	logging.info("\r\n[USER INSTRUCTION]Please add the Pelion Device ID to config.py\r\n")
	logging.info("exiting script")
	raise SystemExit


###############################
# Step 1.3 - Check Treasure Data API Key
###############################
# The purpose of this section to verify data is getting to Treasure Data

import tdclient

if td_apikey=="CHANGE THIS":
	logging.info("[USER INSTRUCTION]]Please add your Treasure Data API key to config.py")
	logging.info("exiting script")
	raise SystemExit

logging.info("\r\n\r\n***** Step 1.3 *******\r\n")
logging.info("We will now check Treasure Data to see if info is successfully making it into the system")
logging.info("If this erros out, please make sure that \n1) you have created a database called "+td_database+"\n2)It may take 3-5min for data to process and appear in the database") 
with tdclient.Client(td_apikey) as client:
    job = client.query(td_database, td_query)
    logging.info("Runnig TD query... Please wait for it to finish (<30sec)...")
    # sleep until job's finish
    job.wait()
    logging.info("Result is")
    for row in job.result():
        logging.info(row)

logging.info("Setup is now complete. Please go on to running the E2E Demo by using e2e.py")

