# import os
# import tdclient

# # Treasure Data Information
# apikey = "10389/599f0416d91cfba4fe1d950e3497e01be258efec" 
# database = "device_health"
# query = "select AVG( cast(total_size as double)) FROM heap_info"

# # Step 2 - Get info from Treasure Data 
# with tdclient.Client(apikey) as client:
#     job = client.query(database, query)
#     print "Runnig TD query... Please wait for it to finish (<30sec)..."
#     # sleep until job's finish
#     job.wait()
#     print "Result is"
#     for row in job.result():
#         print(row)

# # Step 3 - Custom Algorithm

# 	# get the avg value
# x = 0
# for thing in job.result():
# 	x = thing
# value = x[0] 

# Step 4 - Compile new binary with custom #define's
from online_compiler_script import *
mbedUser = "mbed_demo"
mbedPassword = "password2"
# repo = "https://os.mbed.com/teams/mbed_example/code/Compile_API";
repo="https://os.mbed.com/users/coisme/code/Pelion-DM-Workshop-Project"
# target = "ST-Discovery-L475E-IOT01A";
target = "ST-Discovery-L475E-IOT01A"
symbols = "MESSAGE=\"Hello World\",LED=LED2"

build_repo(mbedUser,mbedPassword,repo,target,symbols)


print("finished")

# Step 5 - Send new binary to device via Pelion