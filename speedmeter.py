import os, time, sys, re, json, schedule, subprocess, logging
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

SPEEDTEST_SERVER_ID_LIST = os.environ.get('SPEEDTEST_SERVER_ID_LIST') or ''
if SPEEDTEST_SERVER_ID_LIST != '':
    SPEEDTEST_SERVER_ID_LIST = SPEEDTEST_SERVER_ID_LIST.split(":")
else:
    SPEEDTEST_SERVER_ID_LIST = []

INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST") or 'localhost'
INFLUXDB_PORT = os.environ.get("INFLUXDB_PORT") or 8086
INFLUXDB_USERNAME = os.environ.get("INFLUXDB_USERNAME") or 'your_influxdb_username'
INFLUXDB_PASSWORD = os.environ.get("INFLUXDB_PASSWORD") or 'your_influxdb_password'
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE") or 'network'

SPEEDTEST_INTERVAL_MINUTES = os.environ.get("SPEEDTEST_INTERVAL_MINUTES") or 30
SPEEDTEST_INTERVAL_MINUTES = int(SPEEDTEST_INTERVAL_MINUTES)

SERVER_HOST_NAME = os.environ.get("SERVER_HOST_NAME") or 'raspberrypi-4'

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def test_speed():
    if len(SPEEDTEST_SERVER_ID_LIST) != 0:
        for server_id in SPEEDTEST_SERVER_ID_LIST:
            query_code = 'speedtest --accept-license --accept-gdpr -f json --server-id '+ str(server_id)
            logging.info("Using : " + query_code)
            try:
                response = subprocess.Popen(query_code, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
                data = json.loads(response)
                download = data["download"]["bandwidth"]
                upload = data["upload"]["bandwidth"]
                ping = data["ping"]["latency"]
                break
            except:
                logging.error("Failed to get speed from server ID " + str(server_id))
                continue
    else:
        query_code = 'speedtest --accept-license --accept-gdpr -f json'
        logging.info("Using : " + query_code)
        try:
            response = subprocess.Popen(query_code, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            data = json.loads(response)
            download = data["download"]["bandwidth"]
            upload = data["upload"]["bandwidth"]
            ping = data["ping"]["latency"]
        except:
            logging.error("Failed to fetch : Try using fixed server IDs ")
    
    speed_data = [
        {
            "measurement" : "internet_speed",
            "tags" : {
                "host": SERVER_HOST_NAME
            },
            "fields" : {
                "download": float(download),
                "upload": float(upload),
                "ping": float(ping)
            }
        }
    ]

    client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)

    try:
        logging.info("Result : " + str(speed_data))
        client.write_points(speed_data)
        logging.info("Success: Transfered data points to influxdb")
    except InfluxDBClientError as err:
        logging.error("Influxdb connection failed! " + str(err))

print("Starting speedtest....")
test_speed()
schedule.every(SPEEDTEST_INTERVAL_MINUTES).minutes.do(test_speed) # Auto-speed-test

while True:
    schedule.run_pending()
    time.sleep(5)