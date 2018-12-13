import os
import tdclient
import logging

# configure logging level. 
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)

# # Treasure Data Information
# apikey = "10389/599f0416d91cfba4fe1d950e3497e01be258efec" 
# database = "test_database"
# query = "select AVG( cast(test_table as double)) FROM test_database"
# 
# if apikey=="CHANGE THIS":
# 	logging.info("***Hey, go modify test.py and change the apikey variable or this wont work!***")
# 	logging.info("exiting script")
# 	raise SystemExit

################################
# # Step 2 - Get info from Treasure Data 
################################
# with tdclient.Client(apikey) as client:
#     job = client.query(database, query)
#     print "Runnig TD query... Please wait for it to finish (<30sec)..."
#     # sleep until job's finish
#     job.wait()
#     print "Result is"
#     for row in job.result():
#         print(row)

################################
# # Step 3 - Custom Algorithm
################################

# 	# get the avg value
# x = 0
# for thing in job.result():
# 	x = thing
# algo_value = x[0] 

################################
# Step 4 - Compile new binary with custom #define's
################################
# from online_compiler_script import *
# from connect_dev_credentials import *
# mbedUser = "mbed_demo"
# mbedPassword = "password2"
# # repo = "https://os.mbed.com/teams/mbed_example/code/Compile_API";
# # repo = "https://os.mbed.com/teams/mbed-os-examples/code/mbed-os-example-blinky"
# repo="https://os.mbed.com/users/mbed_demo/code/e2edemo-base"
# # target = "ST-Discovery-L475E-IOT01A";
# target = "ST-Discovery-L475E-IOT01A"
# # symbols = "MESSAGE=\"Hello World\",LED=LED2"+","+connect_macros.replace('\n','')
# symbols = ""
# build_repo(mbedUser,mbedPassword,repo,target,symbols)

import subprocess
import sys

# CHANGE THESE
mbed_cloud_api_key = "CHANGE THIS"
mbed_cloud_device_id = "CHANGE THIS"

mbedos_repo="https://www.github.com/BlackstoneEngineering/mbed-os-example-e2e-demo"
mbedos_repo_projectname = mbedos_repo.split("/")[-1]
logging.debug("project name detected as "+mbedos_repo_projectname)
target = "DISCO_L475VG_IOT01A"
algo_name = "ALGO" # this corresponds to the #define in the main.cpp file

if mbed_cloud_api_key=="CHANGE THIS":
	logging.info("***Hey, go modify test.py and change the mbed_cloud_api_key variable or this wont work!***")
	logging.info("exiting script")
	raise SystemExit

#Check that repo is downloaded
if not os.isdir(mbedos_repo_projectname):
	logging.info("Repo not found, importing it now")
	check = subprocess.check_output("mbed","import",mbedos_repo)
	logging.debug("[MBED IMPORT]"+check)

os.chdir(mbedos_repo_projectname) # change working directory to be inside mbedos repo

# check if update certs are in the project.
if not os.isdir(".update-certificates"):
	# If no update certs, add them (only first time)
	check = subprocess.check_output("mbed", "dm", "init", "-a", mbed_cloud_api_key, "-d", "\"http://os.mbed.com\"", "--model-name", "\"modelname\"", "-q", "--force")
	logging.debug("[Mbed Device Management]"+check)

# Compile the program with algorightm added
logging.info("Adding #define "+algo_name+"="+algo_value+"to the binary")
check=subprocess.check_output("mbed", "compile", "--target", target,"--toolchain", "GCC_ARM","-D"+algoname+"="+algo_value)
logging.debug("[Mbed Compile]"+check)


################################
# Step 5 - Send new binary to device via Pelion
################################

# set Mbed CLoud API key into the environment
logging.info("setting mbed cloud api key into the environment variables")
os.environ["CLOUD_SDK_API_KEY"]=mbed_cloud_api_key
check = subprocess.check_output("mbed", "config", "CLOUD_SDK_API_KEY", mbed_cloud_api_key)

# issue update
# logging.info("running update on device "+mbed_cloud_device_id)
# check = subprocess.check_output("mbed", "dm" ,"update", "device", "-D", mbed_cloud_device_id, "-m", target , "-vv")
# logging.debug("[mbed dm update]"+check)



print("finished")