#!/usr/bin/env python2.7
# Hacky way to pull out Python dictionaries from Ansible ec2 module output

def find_influxdb_instances(output):
    # String we're looking for
    entry_string = "TASK: [Add InfluxDB hosts to inventory] ***************************************"
    # String that marks the end of a boundary
    end_string = "TASK"
    # String that every line should start with
    repeat_string = "ok: [localhost] => (item="
    # Find the start of our string
    start_index = output.find(entry_string) + len(entry_string) + 2
    # Find the end of our string
    end_index = output.find(end_string, start_index + 1)
    # Break up each line between our indices
    lines = output[start_index:end_index].split('\n')
    # Create a list to store our resulting dictionaries
    d = []
    for line in lines:
        if line != "":
            # If line is not empty, find our starting and closing brackets
            start = line.find('{')
            end = line.rfind('}') + 1
            # Store content between brackets
            obj = line[start:end]
            # print obj
            # Convert string to dictionary, and store the results
            d.append(eval(obj))
    return d

def find_stress_instances(output):
    # String we're looking for
    entry_string = "TASK: [Add stress hosts to inventory] *****************************************"
    # String that marks the end of a boundary
    end_string = "PLAY"
    # String that every line should start with
    repeat_string = "ok: [localhost] => (item="
    # Find the start of our string
    start_index = output.find(entry_string) + len(entry_string) + 2
    # Find the end of our string
    end_index = output.find(end_string, start_index + 1)
    # Break up each line between our indices
    lines = output[start_index:end_index].split('\n')
    # Create a list to store our resulting dictionaries
    d = []
    for line in lines:
        if line != "":
            # If line is not empty, find our starting and closing brackets
            start = line.find('{')
            end = line.rfind('}') + 1
            # Store content between brackets
            obj = line[start:end]
            # Convert string to dictionary, and store the results
            d.append(eval(obj))
    return d
    
def main():
    output = None
    with open("../sample-outputs/ansible-output-sample.txt", "rb") as fd:
        output = fd.read()
    d = {}
    d.update( { "influxdb" : [] } )
    d.update( { "stress" : [] } )
    d["influxdb"] = find_influxdb_instances(output)
    d["stress"] = find_stress_instances(output)
    print d

if __name__ == '__main__':
    main()
