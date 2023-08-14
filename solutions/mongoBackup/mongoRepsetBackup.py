import re
import sys
import subprocess
from pymongo import MongoClient

def validate_connection_string():
    # - Parse and check the passed connection string using RegEx
    #     - Validate the connection string is well constructed
    #     - Store the passed information in variables
    #     - If the string is not valid, exit the script

    connection_string_syntax = "mongodb://username:password@host1[:port1][,...hostN[:portN]]/defaultauthdb[?options]"

    # Groups:
    #   0 - username
    #   1 - password
    #   2 - list of hosts
    #   3 - default db
    #   4 - additional options
    connection_string_regex = r"^mongodb:\/\/(\w+):(\S+)@((?:[a-zA-Z0-9_.-]+(?::\d+)?)(?:,[a-zA-Z0-9_.-]+(?::\d+)?)*)\/(\w+)(?:\?((?:\w+=\w+)(?:&\w+=\w+)*))?$"

    if len(sys.argv) != 1:
        sys.exit(
            'Wrong number of arguments!\n'
            'One, and only one, argument is expected, which is a MongoDB connection string that conforms to this syntax:\n' + 
            connection_string_syntax
        )

    matched_connection_string = re.search(connection_string_regex, sys.argv[0])

    if matched_connection_string is None:
        sys.exit(
            'Wrong connection string!\n'
            'Please check that the MongoDB connection string conforms to this syntax:\n' + 
            connection_string_syntax
        )

    parsed_connection_string = {
        "username": matched_connection_string.group(0),
        "password": matched_connection_string.group(1),
        "hosts": matched_connection_string.group(2).split(","),
        "defaultdb": matched_connection_string.group(3),
        "options": matched_connection_string.group(4),
    }

    return parsed_connection_string

def get_mongo_repset_members(connection_string: str):
    # - Use [PyMongo](https://pymongo.readthedocs.io/en/stable/) to connect to the MongoDB replica set
    # - Check that we're connected to a MongoDB replica set
    # - Get the list of members and their priorities
    # - End the connection to the replica set
    # replica_set_hosts = {
    #   "mongo1:27017": { "type": "primary", "priority": 2.0 },
    #   'mongo2:27017': {'type': 'secondary', 'priority': 0.0},
    #   'mongo3:27017': {'type': 'secondary', 'priority': 1.0}
    # }

    client = MongoClient(connection_string)

    if client.primary is None:
        sys.exit(
            'Not a Replica Set!\n'
            'This script assumes that the connection is to a replica set. Please review your connection string and point to replica set'
        )

    replica_set_secondary_nodes = list(client.secondaries)

    if len(replica_set_secondary_nodes) == 0:
        sys.exit(
            'Cannot find a secondary!\n'
            'Either this replica set has no secondaries, or they are all hidden.\n'
            'Please review your deployment or check the connection string.\n'
        )

    replica_set_hosts = {}
    replica_set_hosts[client.primary[0] + ":" + str(client.primary[1])] = {"type": "primary"}
    for secondary in client.secondaries:
        replica_set_hosts[secondary[0] + ":" + str(secondary[1])] = {"type": "secondary"}

    for repset_member in client.admin.command("replSetGetConfig")['config']['members']:
        replica_set_hosts[repset_member["host"]]["priority"] = repset_member["priority"]

    client.close()

    return replica_set_hosts

def backup_mongo_instance(connection_string: str, hostname: str):
    # - Connect to a secondary node
    # - Perform the [`db.fsyncLock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncLock/) on this secondary node
    # - Run the backup script pointing to this node
    # - Once the backup script ends, unlock the instance with [`db.fsyncUnlock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncUnlock/#mongodb-method-db.fsyncUnlock)

    client = MongoClient(connection_string)
    
    # Perform fsyncLock
    client.admin.command('fsync', lock=True)

    # Call backup script
    backup_mongo_process = subprocess.Popen(["./make-vm-snapshot.sh", hostname])
    backup_mongo_process.wait()
    print(backup_mongo_process.communicate())

    # If DB locked unlock it
    if client.admin.command('currentOp').get('fsyncLock'):
        client.admin.command('fsyncUnlock')

    client.close()

def main():
    print("Starting Mongo Replica Set Backup execution\n")

    print("Validating passed parameters\n")
    connection_string_information = validate_connection_string()

    print("Parameters valid\nGathering information of replica set\n")
    replica_set_members = get_mongo_repset_members(sys.argv[0])

    # - Check if any of the secondary members is passive (priority is 0)
    #     - If we have one of these members, this would be the preferred one to run a backup on
    #     - If not, connect to one of the secondary nodes
    chosen_replica_set_node = None
    replica_set_secondaries = []

    for member in replica_set_members:
        if replica_set_members[member]["type"] == "secondary":
            replica_set_secondaries.append(member)
            if replica_set_members[member]["priority"] == 0:
                chosen_replica_set_node = member
                break
    
    chosen_replica_set_node = chosen_replica_set_node if chosen_replica_set_node is not None else replica_set_secondaries[0]

    print("Got MongoDB replica set information\nStarting backup process\n")
    connection_options_without_repset = [
        option
        for option in connection_string_information["options"].split("&")
        if "replicaSet" not in option]
    connection_options_without_repset = "&".join(connection_options_without_repset)
    
    secondary_node_connection_string = "mongodb://{}:{}@{}/{}?{}".format(
        connection_string_information["username"],
        connection_string_information["password"],
        chosen_replica_set_node,
        connection_string_information["defaultdb"],
        connection_options_without_repset
    )

    backup_mongo_instance(secondary_node_connection_string, chosen_replica_set_node)

    print("Backup completed with success!\n")
    return

if __name__ == "__main__":
    main()
