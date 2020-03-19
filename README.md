# Packet Device Tester
This repo contains a python script: `device_builder.py`. That will create devices of a certain `plan`, `quantity`, & `operating system` into given `facilities`. If all goes well all resources will be cleaned up automatically.
## Prerequisites
There is only one python module needed to run this script: `packet-python`
You will also need your Packet API Key as well as your Organization ID.
These can be passed in via the command line, but these can also be pulled from enviorment variables as follows:
```bash
export PACKET_TOKEN="guRDYrg6nLgSvoZuB8UYSh5mAHFACTHR"
export PACKET_ORG_ID="erd6e156-e5fb-4e5b-b90e-090a055437ee"
```
## Usage
```bash 
device_builder.py --facility <facility_list> --plan <device_plan> --os <operating_system>
                  [--quantity <number>] [--api_key <api_key>] [--org_id <org_id>]
                  [--project_name <project_name>]
```
If quantity is omitted only one device will be deployed. The default project name is `packet_device_tester`
## Options
  ```bash
  -h, --help                     show this help message and exit
  --facility=FACILITY            List of facilities to deploy servers. 
                                   Example: ewr1,sjc1
  --plan=PLAN                    Device plan to deploy. 
                                   Example: c3.small.x86
  --os=OS                        Operating System to deploy on the Device. 
                                   Example: ubuntu_18_04
  --quantity=QUANTITY            Number of devices to deploy per facility. 
                                   Example: 100
  --api_key=API_KEY              Packet API Key. 
                                   Example: vuRQYrg2nLgSvoYuB8UYSh4mAHFACTHB
  --org_id=ORG_ID                Packet Organization ID. 
                                   Example: ecd8e248-e2fb-4e5b-b90e-090a055437dd
  --project_name=PROJECT_NAME    Project Name to be created. 
                                   Example: my-best-project
```

## Getting results
Results are stored in a MySQL database on a Kubernetes node. Grafana has been deployed on this cluster to help visualize and build dashboards and reports. You can access Grafana at https://packet.codyhill.co/grafana

