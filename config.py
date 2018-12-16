mbed_cloud_api_key = "ak_1MDE1ZWNlMGNiY2Y2MDI0MjBhMDE0ZTBhMDAwMDAwMDA016781de1cd72e624181b8a300000000e1JePFRfVnEC7MAJO1aUrwqa53USBH4Q"
mbed_cloud_device_id = "CHANGE THIS"

td_apikey = "10389/599f0416d91cfba4fe1d950e3497e01be258efec" 
td_database = "test_database"
td_query = "select AVG( cast(temp as double)) FROM test_table"


mbedos_repo="https://www.github.com/BlackstoneEngineering/mbed-os-example-e2e-demo"
mbedos_repo_projectname = mbedos_repo.split("/")[-1]
target = "DISCO_L475VG_IOT01A"
algo_name = "ALGO" # this corresponds to the #define in the main.cpp file