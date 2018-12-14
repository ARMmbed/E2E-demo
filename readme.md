## Intro
This is a complete End to End ecosystem demo for the Arm Pelion IoT Platform family of services. This proof of concept implementation (not ready for production) sends data from Mbed OS to Treasure Data. A query is run on the data to generate a new algorithm, which is then compiled into a new binary which is then sent to the device using the Pelion Device Management Update Service. 

![Picture of it working](TODO)


## Requirements
1) [Mbed CLI](https://os.mbed.com/docs/v5.9/tools/installation-and-setup.html) Version 1.8.3+ 
2) [Treasure Data Python Client](https://support.treasuredata.com/hc/en-us/articles/360001264848-Python-Client) (td-client) `pip install td-client`


## Setup
### Treasure Data
1) Get your Treasure Data API Key
2) Create a database called 'test_database'
3) Fill in the TD Variables at the top of `test.py` (database name, table name, TD API Key)

### Mbed OS
3) Add your Pelion Device Management API key to `test.py` (Cloud Portal)[http://portal.mbed.cloud.com]  (Access Management -> API Keys -> +New API Key, make sure its an admin key)
4) Run the script. It will download the mbed-os program, initialize it with certificates
5) Change `mbed-os-example-e2e-demo/mbed_app.json`, you will need to add your TD API key, Wifi SSID and Wifi Password here.
6) Run the script again, this time it will compile the program
7) Load the initial program onto the device by copy / pasting the binary from the `mbed-os-example-e2e-demo/BUILD/<TargetName>/GCC/mbed-os-example-e2e-demo.bin` to the board. (This will make sure you have the same update credentials on the board that you do on the device). Wait for the LED to stop flashing before proceeding to step 8.
8) Reset the device and wait for it to connect to the Pelion Portal (you can monitor the output by running `mbed sterm -b 115200` from inside the `mbed-os-example-e2e-demo` folder)
9) Copy the Device ID from the portal into the `mbed_cloud_device_id` variable in `test.py` 
10) Now run the script with the `python test.py` command and it *should* just work. 


## Running it after setup
After the initial setup (filling in all the variables and getting the update certs onto the device) you can trivially deploy your algorithm to the device by simply running test.py. It wil automatically ping Treasure Data, compile a new binary, and then load the code to the device via update. 

Please note that if you change your SSID / Password for the wifi you will need to recompile the binary as outlined in steps 5-7.


## Limitations
- must be run on local machine connected to the internet. 
- pain in the ass to use. 


## Troubleshooting
- Turn on more verbose debugging in test.py by changing `INFO` to `DEBUG` in `logging.basicConfig(level=logging.DEBUG)`


## Future Improvement
- move away from mbed CLI to dockerized service
- increase scripting so user doesnt have to manually input all the variables
- Add 'typename' to the endpoints so every endpoint gets updated by type instead of by individual device ID
- Create single page website for this so its all GUI based instead of command line based. 

