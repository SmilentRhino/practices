#!/usr/bin/env python3

"""This is a simple script to list aws reserved instances and running instances
in a table, or csv file.
aws ec2 --region cn-north-1 --output json \
        describe-instances >/home/mzzhang/runningtmp1
aws ec2 --region cn-north-1 --output json \
        describe-reserved-instances  > /home/mzzhang/reservedtmp1
as our subaccounts can only see the running instances of its own, we have
serveral runningtmp* files
and all reserved instance is list in reservedtmp1
I suggetst use boto3 to get the response instead of awscli
"""

import json
import glob

with open('/Users/mzzhang/aws_ri/reservedtmp1', 'r') as f:
    RESERVED_INSTANCES = f.read()
RESERVED_INSTANCES = json.loads(RESERVED_INSTANCES)

RUNNING_LISTS = glob.glob('/Users/mzzhang/aws_ri/running*')
RUNNING_LIST = []
for rl in RUNNING_LISTS:
    with open(rl, 'r') as f:
        reservations = f.read()
        reservations = json.loads(reservations)
        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                RUNNING_LIST.append(instance)

RESULT = {}

for ri in RESERVED_INSTANCES['ReservedInstances']:
    if ri["State"] == 'active':
        if ri["InstanceType"] not in RESULT.keys():
            RESULT[ri["InstanceType"]] = {
                "RESERVED_INSTANCES" : [ri]*ri["InstanceCount"],
                "runnings" : []}
        else:
            RESULT[ri["InstanceType"]]["RESERVED_INSTANCES"].extend(
                [ri]*ri["InstanceCount"])

for running in RUNNING_LIST:
    if running["State"]["Name"] == 'running':
        if running["InstanceType"] not in RESULT.keys():
            RESULT[running["InstanceType"]] = {
                "RESERVED_INSTANCES" : [],
                "runnings" : [running]}
        else:
            RESULT[running["InstanceType"]]["runnings"].append(running)

for k in sorted(RESULT.keys()):
    if RESULT[k]['RESERVED_INSTANCES']:
        ri_count = len(RESULT[k]['RESERVED_INSTANCES'])
    else:
        ri_count = 0
    if RESULT[k]['runnings']:
        running_count = len(RESULT[k]['runnings'])
    else:
        running_count = 0
    for i in range(max(ri_count, running_count)):
        print(k, end='\t')
        if i < ri_count:
            print(RESULT[k]['RESERVED_INSTANCES'][i]['Start'],
                  '\t',
                  RESULT[k]['RESERVED_INSTANCES'][i]['End'],
                  end='\t'
                 )
            if RESULT[k]['RESERVED_INSTANCES'][i]['Scope'] == 'Region':
                print('Region', end='\t')
            else:
                print(RESULT[k]['RESERVED_INSTANCES'][i]['AvailabilityZone'], end='\t')
        else:
            print('\t'*2, end='\t')
        if i < running_count:
            print('\t'.join(
                sorted(
                    [':'.join(j.values()) for j in RESULT[k]['runnings'][i]['Tags']])))
        else:
            print()

