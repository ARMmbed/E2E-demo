## Intro
This is a complete End to End ecosystem demo for the Arm Pelion IoT Platform family of services. This proof of concept implementation (not ready for production) sends data from Mbed OS to Treasure Data. A query is run on the data to generate a new algorithm, which is then compiled into a new binary (using macro's and the magical `-DMACRO=VALUE` command) which is then sent to the device using the Pelion Device Management Update Service. 

Please note that you should first run `python setup.py` to setup the system, then run `python e2e.py` after that each time you want to update the device / run the demo. 

![Picture of it working](TODO)


## Requirements
1) [Mbed CLI](https://os.mbed.com/docs/v5.9/tools/installation-and-setup.html) Version 1.8.3+ 
2) [Treasure Data Python Client](https://support.treasuredata.com/hc/en-us/articles/360001264848-Python-Client) (td-client) `pip install td-client`


## Setup.py
### Treasure Data
1) Get your Treasure Data API Key
2) Create a database called 'test_database'
3) Fill in the TD Variables at the top of `config.py` (database name, table name, TD API Key)

### Mbed OS

#### Clone example
3) Add your Pelion Device Management API key to `config.py` (Cloud Portal)[http://portal.mbed.cloud.com]  (Access Management -> API Keys -> +New API Key, **make sure its an admin key**)
4) Run the `setup.py` script. It will download the mbed-os program, initialize it with certificates

#### Modify wifi / TD API settings
5) Change `mbed-os-example-e2e-demo/mbed_app.json`, you will need to add your TD API key, Wifi SSID and Wifi Password here.

#### Flash code / get Device ID
6) Run the script again, this time it will compile the program and load it onto your baord. Wait for the LED to stop flashing before proceeding to step 7.
7) Reset the device (press the reset button) and wait for it to connect to the Pelion Portal (you can monitor the output by running `mbed sterm -b 115200` from inside the `mbed-os-example-e2e-demo` folder or by using putty, coolterm or tera term, whatever your preference is)
9) Copy the Device ID from the portal into the `mbed_cloud_device_id` variable in `config.py` 

## E2E.py
After the initial setup (of setup.py) (filling in all the variables and getting the update certs onto the device) you can trivially deploy your algorithm to the device by simply running test.py. It wil automatically ping Treasure Data, compile a new binary, and then load the code to the device via update. 

Please note that if you change your SSID / Password for the wifi you will need to recompile the binary by following the instructions from step 5. 

## Customizing the Algorithm
If you want to make a more custom algorithm (the default is just an average of a column in a table) then you should modify the code in step 2.1 and 2.2 of 'e2e.py'. The underlying framework does not care what you do, as long as it can run string replacement on it. 

If you want to pass in multiple values (currently we are just sharing 1 thing, the average, in a macro called `ALGO`), you will need to create additional `#define MACRO VALUE` in the main.cpp file as well as pass them in in step 2.3 by adding additional `-DMACRO=VALUE` commands to the `mbed compile ..... -DMACRO1=VALUE1 -DMACRO2=VALUE2 -DMACRO3=VALUE3` command. 

## Scheduled Updates
At the moment there is no in-built functionality for scheduled updates. To acheive this i suggest setting up a cron job that runs the e2e.py script every hour or every 10min or whatever period of time you want. 

## Limitations
- must be run on local machine connected to the internet. 
- pain in the ass to use. 


## Troubleshooting
- Turn on more verbose debugging in test.py by changing `INFO` to `DEBUG` in `logging.basicConfig(level=logging.DEBUG)`


## Future Improvement
- move away from mbed CLI to dockerized service
- increase automation to reduce number of steps
- increase scripting so user doesnt have to manually input all the variables
- Add 'typename' to the endpoints so every endpoint gets updated by type instead of by individual device ID
- Create single page website for this so its all GUI based instead of command line based. 
- Move WIFI SSID / Password into #defines so user doesnt have to config them in mbed_app.json
- Various enhancements to make this process faster (move algo to be defined globally so it doesnt recompile from scratch each time,...etc)

