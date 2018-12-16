mbed_cloud_api_key = "CHANGE THIS"
mbed_cloud_device_id = "CHANGE THIS"

td_apikey = "CHANGE THIS" 
td_database = "test_database"
td_query = "select AVG( cast(temp as double)) FROM test_table"


mbedos_repo="https://www.github.com/BlackstoneEngineering/mbed-os-example-e2e-demo"
mbedos_repo_projectname = mbedos_repo.split("/")[-1]
target = "DISCO_L475VG_IOT01A"
algo_name = "ALGO" # this corresponds to the #define in the main.cpp file