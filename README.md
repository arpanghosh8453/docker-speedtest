# docker-speedtest
Checks the internet speed using Ookla speedtes CLI and writes the data to a local influxdb database

If you have a preconfigured influxdb instance, simply run the following docker compose with 'docker compose up -d' 

docker
```
version: '3.4'
services:
  python-speedtest:
    restart: unless-stopped
    image: thisisarpanghosh/python-speedtest:latest
    container_name: python-speedtest
    hostname: python-speedtest
    environment:
      - INFLUXDB_HOST=influxdb
      - INFLUXDB_PORT=8086
      - INFLUXDB_USERNAME=your_influxdb_username
      - INFLUXDB_PASSWORD=your_influxdb_password
      - INFLUXDB_DATABASE=network # You need the database with this name ready
      - SPEEDTEST_INTERVAL_MINUTES=30
      # Optional : Use only if you want to use specific test servers - use : as seperator between IDs
      #- SPEEDTEST_SERVER_ID_LIST=17394:19249:13180:3752:8913:3639:17828
      - SERVER_HOST_NAME=your_machine_name # Can be anything, e.g. raspberrypi
```
