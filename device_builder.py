#!/usr/bin/env python

import optparse
import sys
import packet
import os
import json
from time import sleep
from http import client as httplib
from datetime import datetime as dt


def parse_args():
    parser = optparse.OptionParser(
        usage="\n\t%prog --facility <facility_list> --plan <device_plan> --os <operating_system>"
              "\n\t\t\t[--quantity <number>] [--api_key <api_key>] [--project_id <project_id>]")
    parser.add_option('--facility', dest="facility", action="store",
                      help="List of facilities to deploy servers. Example: ewr1,sjc1")
    parser.add_option('--plan', dest="plan", action="store",
                      help="Device plan to deploy. Example: c3.small.x86")
    parser.add_option('--os', dest="os", action="store",
                      help="Operating System to deploy on the Device. Example: ubuntu_18_04")
    parser.add_option('--quantity', dest="quantity", action="store", default=1,
                      help="Number of devices to deploy per facility. Example: 100")
    parser.add_option('--api_key', dest="api_key", action="store", default=None,
                      help="Packet API Key. Example: vuRQYrg2nLgSvoYuB8UYSh4mAHFACTHB")
    parser.add_option('--project_id', dest="project_id", action="store", default=None,
                      help="Packet Project ID. Example: ecd8e248-e2fb-4e5b-b90e-090a055437dd")
    # TODO: There migth be a desire to not cleanup... Maybe I should add a --skip-cleanup flag.

    options, _ = parser.parse_args()
    if not (options.facility and options.plan and options.os):
        print("ERROR: Missing arguments")
        parser.print_usage()
        sys.exit(1)

    if not options.api_key:
        options.api_key = os.getenv('PACKET_TOKEN')

    if not options.api_key:
        print("ERROR: API Key is required ether pass it in via the command line or export 'PACKET_TOKEN'")
        sys.exit(1)

    if not options.project_id:
        options.project_id = os.getenv('PACKET_PROJECT_ID')

    if not options.project_id:
        print("ERROR: Project ID is required ether pass it in via the command line or export 'PACKET_PROJECT_ID'")
        sys.exit(1)
    try:
        options.quantity = int(options.quantity)
    except ValueError:
        print("ERROR: Quantity must be a valid integer. Example: 5")
        sys.exit(1)
    # TODO: We need to validate user input that things exist... Operating System, Plan, Facility, etc...
    options.facilities = options.facility.split(",")
    return options


def authenticate(args):
    manager = packet.Manager(auth_token=args.api_key)
    auth = False
    try:
        organizations = manager.list_organizations()
        auth = True
    except packet.baseapi.Error:
        auth = False

    if auth is False:
        print("ERROR: Could not validate Auth Token.")
        sys.exit(1)
    return manager


def do_request(action, host, relative_url, headers, body):
    conn = httplib.HTTPSConnection(host)
    body_json = json.JSONEncoder().encode(body)
    conn.request(action, relative_url, body_json, headers)
    response = conn.getresponse()
    return conn, response


def insert_record(body):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": "222b7564-a0f8-4d90-84a9-5a9f4684b3ea"
    }
    _, response = do_request("POST", "packet.codyhill.co", "/insert", headers, body)
    if response.status != 200 and response.status != 201:
        print("Error inserting record!")
        print("{}: {}".format(response.status, response.reason))
        sys.exit(1)


def create_devices(args, manager):
    devices = []
    for i in range(args.quantity):
        for facility in args.facilities:
            hostname = "tester-{}-{}".format(facility, i)
            print("Creating {}".format(hostname))
            try:
                devices.append(manager.create_device(args.project_id, hostname, args.plan, facility, args.os))
            except packet.baseapi.Error as e:
                print(e)
                print("\tError creating device: {}. Skipping...".format(hostname))

    return devices


def poll_devices(args, manager, devices):
    while len(devices) != 0:
        for device in devices:
            print("Checking if {} is active".format(device['hostname']))
            poll_device = manager.get_device(device['id'])
            if poll_device['state'] == 'active':
                print("{} is active!".format(poll_device['hostname']))
                create = dt.strptime(poll_device['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                finish = dt.strptime(poll_device['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
                duration = (finish-create).total_seconds()
                insert_record({
                    'uuid': poll_device['id'],
                    'state': poll_device['state'],
                    'hostname': poll_device['hostname'],
                    'facility': poll_device['facility']['code'],
                    'plan': poll_device['plan']['slug'],
                    'operating_system': poll_device['operating_system']['slug'],
                    'created_at': create.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': finish.strftime('%Y-%m-%d %H:%M:%S'),
                    'creation_duration': duration
                })
                devices.remove(device)
                print("Deleting {}!".format(poll_device['hostname']))
                poll_device.delete()
        sleep(1)
    print("All devices are deleted!")


def validate_args(args, manager):
    os_list = manager.list_operating_systems()
    plan_list = manager.list_plans()
    facility_list = manager.list_facilities()

    os_valid = False
    for op_system in os_list:
        if op_system.slug == args.os:
            os_valid = True
            break
    if os_valid is False:
        print("ERROR: {} is not a valid operating system!".format(args.os))
        sys.exit(1)

    plan_valid = False
    for plan in plan_list:
        if plan.slug == args.plan or plan.name == args.plan:
            plan_valid = True
            break
    if plan_valid is False:
        print("ERROR: {} is not a valid plan!".format(args.plan))
        sys.exit(1)

    for site in args.facilities:
        facility_valid = False
        for facility in facility_list:
            if facility.code == site:
                facility_valid = True
                break
        if facility_valid is False:
            print("ERROR: {} is not a valid facility!".format(site))
            sys.exit(1)


def main():
    args = parse_args()
    manager = authenticate(args)
    print("Authenticated successfully.")
    validate_args(args, manager)
    print("Command line arguments are valid.")
    devices = create_devices(args, manager)
    print("All devices created!")
    poll_devices(args, manager, devices)
    print("All devices have completed.")
    print("Done!")


if __name__ == "__main__":
    main()
