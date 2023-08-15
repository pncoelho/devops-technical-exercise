import re
import sys
import subprocess
from time import sleep
from pymongo import MongoClient

# Groups:
#   0 - connection string
#   1 - username
#   2 - password
#   3 - list of hosts
#   4 - default db
#   5 - additional options
connection_string_regex = r"^mongodb:\/\/(\w+):(\S+)@((?:[a-zA-Z0-9_.-]+(?::\d+)?)(?:,[a-zA-Z0-9_.-]+(?::\d+)?)*)\/(\w+)?(?:\?((?:\w+=\w+)(?:&\w+=\w+)*))?$"
connection_string_syntax = "mongodb://username:password@host1[:port1][,...hostN[:portN]]/defaultauthdb[?options]"
backup_script_path = "./make-vm-snapshot.sh"

def validate_connection_string(connection_string: str):
    """Parse and check the passed connection string using RegEx

    Perform a regex validation of the connection string.
    
    Returns the connection string converted to a dictionary
    """

    matched_connection_string = re.search(connection_string_regex, connection_string)

    if matched_connection_string is None:
        sys.exit(
            'Wrong connection string!\n'
            'Please check that the MongoDB connection string conforms to this syntax:\n' + 
            connection_string_syntax
        )

    parsed_connection_string = {
        "username": matched_connection_string.group(1),
        "password": matched_connection_string.group(2),
        "hosts": matched_connection_string.group(3).split(","),
        "defaultdb": matched_connection_string.group(4),
        "options": matched_connection_string.group(5),
    }

    return parsed_connection_string

def get_mongo_repset_members(connection_string: str):
    """Get a MongoDB replica set members

    Use PyMongo to connect to the passed connection string and retrieve 
    the list of replica set members

    Returns a dictionary with the members, their type (primary or secondary) 
    and their priority
    Example:
        replica_set_hosts = {
            "mongo1:27017": { "type": "primary", "priority": 2.0 },
            'mongo2:27017': {'type': 'secondary', 'priority': 0.0},
            'mongo3:27017': {'type': 'secondary', 'priority': 1.0}
        }
    """

    print("Connecting to replica set with the following connection string:\n{}\n".format(
        connection_string))
    client = MongoClient(connection_string)

    # Just to ensure the MongoClient has retrieved the node information
    # https://pymongo.readthedocs.io/en/stable/examples/high_availability.html#id1
    sleep(0.1);

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

    print("Connection successful.\nGathering replica set member information.\n")

    replica_set_hosts = {}
    replica_set_hosts[client.primary[0] + ":" + str(client.primary[1])] = {"type": "primary"}
    for secondary in client.secondaries:
        replica_set_hosts[secondary[0] + ":" + str(secondary[1])] = {"type": "secondary"}

    # Use replica set configuration to get member's priorities
    for repset_member in client.admin.command("replSetGetConfig")['config']['members']:
        replica_set_hosts[repset_member["host"]]["priority"] = repset_member["priority"]

    print("Information gathered, closing connection.\n")
    client.close()

    return replica_set_hosts

def backup_mongo_instance(connection_string: str, hostname: str):
    """Perform a consistent backup of a MongoDB instance

    Connects to the instance specified in the connection string, 
    locks the instance, calls the backup script and unlocks the DB.
    """

    print("Connecting to MongoDB node with the following connection string:\n{}\n".format(
        connection_string))
    client = MongoClient(connection_string)
    
    # Perform fsyncLock
    print("Locking {}'s database for backup!\n".format(hostname))
    client.admin.command('fsync', lock=True)

    # Call backup script
    print("Calling {} script for backup on {}\n".format(backup_script_path, hostname))
    backup_mongo_process = subprocess.Popen([backup_script_path, hostname])
    backup_mongo_process.wait()
    print("Backup command output:\n{}\n".format(
        backup_mongo_process.communicate()
    ))

    # Check if DB is still locked
    if client.admin.command('currentOp').get('fsyncLock'):
        # Unlock DB
        print("Unlocking {}'s database.\n".format(hostname))
        client.admin.command('fsyncUnlock')

    client.close()

def main():
    print("Starting Mongo Replica Set Backup execution\n")

    print("Validating passed parameters\n")
    if len(sys.argv) != 2:
        sys.exit(
            'Wrong number of arguments!\n'
            'One, and only one, argument is expected, which is a MongoDB connection string that conforms to this syntax:\n' + 
            connection_string_syntax
        )

    passed_connection_string = sys.argv[1]

    connection_string_information = validate_connection_string(passed_connection_string)

    print("Parameters valid\nGathering information of replica set\n")
    replica_set_members = get_mongo_repset_members(passed_connection_string)

    print("Choosing which secondary node to connect to.\n")
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
    print("Performing backup on {}.\n".format(chosen_replica_set_node))

    # Check if the replicaSet option was passed to the initial connection string
    # if it was, remove it from the list of options
    connection_options_without_repset = [
        option
        for option in connection_string_information["options"].split("&")
        if "replicaSet" not in option]
    connection_options_without_repset = "&".join(connection_options_without_repset)
    
    # Create connection string to connect to chosen secondary
    secondary_node_connection_string = "mongodb://{}:{}@{}/{}?{}".format(
        connection_string_information["username"],
        connection_string_information["password"],
        chosen_replica_set_node,
        connection_string_information["defaultdb"],
        connection_options_without_repset
    )

    print("Got MongoDB replica set information\nStarting backup process\n")
    backup_mongo_instance(secondary_node_connection_string, chosen_replica_set_node)

    print("Backup completed with success!\n")
    return

if __name__ == "__main__":
    main()
