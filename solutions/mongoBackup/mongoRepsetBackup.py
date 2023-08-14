def validate_connection_string():
    # - Parse and check the passed connection string using RegEx
    #     - Validate the connection string is well constructed
    #     - Store the passed information in variables
    #     - If the string is not valid, exit the script
    # TODO: create and call method to check passed parameters and return dict with information
    return dict()

def get_mongo_repset_members(connection_string: str):
    # - Use [PyMongo](https://pymongo.readthedocs.io/en/stable/) to connect to the MongoDB replica set
    # - Check that we're connected to a MongoDB replica set
    # - Get the list of members and their priorities
    # - End the connection to the replica set
    # - Check if any of the secondary members is passive (priority is 0)
    #     - If we have one of these members, this would be the preferred one to run a backup on
    #     - If not, connect to one of the secondary nodes
    """
    TODO:
    create and call method to:
        - connect to a MongoDB instance using the passed connection string
        - Check if the instance is a replica set
        - Return a list of set members, their type and priorities
    """
    return dict()

def backup_mongo_instance(connection_string: str):
    # - Connect to a secondary node
    # - Perform the [`db.fsyncLock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncLock/) on this secondary node
    # - Run the backup script pointing to this node
    # - Once the backup script ends, unlock the instance with [`db.fsyncUnlock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncUnlock/#mongodb-method-db.fsyncUnlock)
    # TODO: Create and call method
    return

def main():
    print("Starting Mongo Replica Set Backup execution\n")

    print("Validating passed parameters\n")
    connection_string_information = validate_connection_string()

    print("Parameters valid\nGathering information of replica set\n")
    replica_set_members = get_mongo_repset_members(sys.argv[0])

    print("Got MongoDB replica set information\nStarting backup process\n")
    secondary_node_connection_string = ""
    backup_mongo_instance(secondary_node_connection_string)

    print("Backup completed with success!\n")
    return

if __name__ == "__main__":
    main()
