# Packet Device Tester
This repo contains a python script: `device_builder.py`. That will create devices of a certain `plan`, `quantity`, & `operating system` into given `facilities`. If all goes well all resources will be cleaned up automatically. You must be `Packet Staff` to us this tool.
## Prerequisites
There is only one python module needed to run this script: `packet-python`
You will also need your Packet API Key, Consumer Token, & Project ID.
**Note:** The `PACKET_CONSUMER_TOKEN` can be retrieved from the staff portal under `Settings > Applications > Packet Portal`
These can be passed in via the command line, but these can also be pulled from enviorment variables as follows:
```bash
export PACKET_AUTH_TOKEN="guRDYrg6nLgSvoZuB8UYSh5mAHFACTHR"
export PACKET_CONSUMER_TOKEN="8wtcigw6j1px9obscksorhpn48gz3evbgoqizcnsm7t7wdsjfmy00a3ng9p8t1d4"
export PACKET_PROJECT_ID="erd6e156-e5fb-4e5b-b90e-090a055437ee"
```
## Usage
```bash 
device_builder.py --facility <facility_list> --plan <device_plan> --os <operating_system>
                  [--quantity <number>] [--api_key <api_key>] [--project_id <project_id>]
                  [--consumer_token <consumer_token>
```
### Notes:
* If ***quantity*** is omitted, only one device will be deployed.
* If ***quantity*** is **all**, every device in each facility will be deployed.
* If ***api_key***, ***project_id***, or ***consumer_token*** are omitted, they are expected to be exported as shown above.
## Options
  ```bash
Options:
  -h, --help                          show this help message and exit
  --facility=FACILITY                 List of facilities to deploy servers. Example: ewr1,sjc1
  --plan=PLAN                         Device plan to deploy. Example: c3.small.x86
  --os=OS                             Operating System to deploy on the Device. Example: ubuntu_18_04
  --quantity=QUANTITY                 Number of devices to deploy per facility. Example: 100
  --api_key=API_KEY                   Packet API Key. Example: vuRQYrg2nLgSvoYuB8UYSh4mAHFACTHB
  --project_id=PROJECT_ID             Packet Project ID. Example: ecd8e248-e2fb-4e5b-b90e-090a055437dd
  --consumer_token=CONSUMER_TOKEN     Packet Consumer Token. Example: 8wtcigw6j1px9obscksorhpn48gz3evbgoqizcnsm7t7wdsjfmy00a3ng9p8t1d4
```

## Getting results
Results are stored in a MySQL database on a Kubernetes node. Grafana has been deployed on this cluster to help visualize and build dashboards and reports. You can access Grafana at https://packet.codyhill.co/grafana


# TODO
* Build some logic to stop checking if servers are finished after X time
  * This should be an overrideable timout with a commandline arg somehting like: --timeout 3600
* Start breaking servers during the provisioning process and see what happens...
  * We should then build in error handling and insert these errors into the DB (Different table?)
* Some work has been started on putting real authentication into the db_inserter
  * Make the db_inserter authenticate as `staff`
  * Update device_builder to pass X-Auth-Token, X-Consumer-Token, & X-Packet-Staff