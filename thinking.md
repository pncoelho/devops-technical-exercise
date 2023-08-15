# Thought Process

## For 1. Consistent Backup Script

When it comes to performing a backup of a MongoDB instance (whether solo instance or replica set), we need to have a consistent database.

In order to achieve this we need to use `db.fsyncLock()` which does the following, as stated in the MongoDB documentation:

> Forces the `mongod` to **flush all pending write** operations to disk and **locks the** entire `mongod` **instance** to prevent additional writes until the user releases the lock with a corresponding `db.fsyncUnlock()` command.

From what is said in the exercise, we have a *script that takes care of the backup part* of the process, so **we need to take care** only **of the locking of the database**

We **already know what our output will be** (a backup of a replica set secondary node, by using the provided script), so **we need to look at our inputs** before we can think about the wrapper script workflow

From the exercise we know that the wrapper script will be passed a MongoDB connection string:

`“mongodb://admin:password@vm-hostname1,vm-hostname2,vm-hostname3/admin?otherParams”`

Let's first deconstruct this connection string (using the [connection-string](https://www.mongodb.com/docs/manual/reference/connection-string/) and [connect](https://www.mongodb.com/docs/mongodb-shell/connect/) MongoDB pages):
- `mongodb://`: The *protocol* to use for the connection, which is MongoDB
- `admin:password`: *Username* and *password* for authentication
- `vm-hostname1,vm-hostname2,vm-hostname3`: *List of hosts* to connect
- `/admin`: This is the *default database* that will be used (`defaultauthdb` option)
- `?otherParams`: These will be *additional connection options*

Since the *protocol* is `mongodb://` and not `mongodb+srv://`, I would assume that one of the *connection options* passed would be the `replicaSet` option

Knowing the desired output and having reviewed the inputs, we can think of the workflow for the wrapper script:
1. Parse and check the passed connection string using RegEx
   1. Validate the connection string is well constructed
   2. Store the passed information in variables
   3. If the string is not valid, exit the script
2. Use [PyMongo](https://pymongo.readthedocs.io/en/stable/) to connect to the MongoDB replica set
3. Check that we're connected to a MongoDB replica set
4. Get the list of members and their priorities
5. End the connection to the replica set
6. Check if any of the secondary members is passive (priority is 0)
   1. If we have one of these members, this would be the preferred one to run a backup on
   2. If not, connect to one of the secondary nodes
7. Connect to a secondary node
8. Perform the [`db.fsyncLock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncLock/) on this secondary node
9. Run the backup script pointing to this node
10. Once the backup script ends, unlock the instance with [`db.fsyncUnlock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncUnlock/#mongodb-method-db.fsyncUnlock)
11. End the script
