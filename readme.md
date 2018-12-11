## Intro
This is a complete End to End ecosystem demo for the Arm Pelion IoT Platform family of services. This proof of concept implementation (not ready for production) sends data from Mbed OS to Treasure Data. A query is run on the data to generate a new algorithm, which is then compiled into a new binary which is then sent to the device using the Pelion Device Management Update Service. 

![Picture of it working](TODO)


## Requirements
1) [Mbed CLI](https://os.mbed.com/docs/v5.9/tools/installation-and-setup.html)
2) [Treasure Data Python Client](https://support.treasuredata.com/hc/en-us/articles/360001264848-Python-Client) (td-client) `pip install td-client`
3) [Mbed Compile API](https://github.com/ARMmbed/mbed-compile-api-js)


## How to use
### Treasure Data
1) Get your Treasure Data API Key
2) Fill in the TD Variables at the top of `test.py` (database name, table name, TD API Key)

### Mbed OS
3) Get a certificate from [portal.mbedcloud.com](https://portal.mbedcloud.com/identity/certificates/developer/new). You will need to download the entire certificate and replace the equivalent lines in connect_cert.py. 


## Limitations
- Device code repo's must be hosted on os.mbed.com (the remote compile service does not support github repos due to legacy reasons)


## Debugging
- The online compiler is currently being migrated, this may lead to your username/password not working, this can be resolved by changing your password or by using the default one provided to a known working account


## Future Improvement
- Swap out the online compiler service for a docker container of mbed CLI, this will enable any repo (github) to be used. It will also be more fail resistant and provide a more solid uptime as well as more control options
- 


https://os.mbed.com/users/mbed_demo/code/e2edemo-base/