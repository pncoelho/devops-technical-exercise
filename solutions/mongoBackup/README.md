# Consistent backups script

This folder contains the proposed solution to the exercise and files to create a testing environment.

## Solution

The **solution can be found in** the [mongoRepsetBackup.py python script](./mongoRepsetBackup.py).

If you intend to run it, *please have a look at the script itself* and **don't forget to install the** [requirements file](./requirements.txt).

## Testing

In order to ensure that the script actually functioned, a testing environment was created.

This environment is:
- A **MongoDB replica set with 3 nodes**
  - *1 primary*
  - *1 secondary*
  - *1 passive secondary*
- Deployed in **docker** containers
- Using **docker-compose**

Most of the structure is copied from the [How to deploy a MongoDB replica set using docker-compose Medium post](https://blog.devgenius.io/how-to-deploy-a-mongodb-replicaset-using-docker-compose-a538100db471), with a few adaptations to the latest version of MongoDB.

To run the environment you just need to run the [start cluster helper script](./startReplicaSetEnvironment.sh) (*you'll need to have docker installed*).

### Describing the Testing Environment

In terms of files we have:
- [`docker-compose-replicaset.yml`](./docker-compose-replicaset.yml) - Docker compose file specifying the 3 node replica set 
  - Also mounts volumes on the primary node for provisioning the replica set
- [`scripts/`](./scripts/) - Directory to store docker compose provisioning scripts (in our case replica set provisioning scripts)
- [`startReplicaSetEnvironment.sh`](./startReplicaSetEnvironment.sh) - A helper script to launch the services and run the provisioning scripts on the primary node
- [`Dockerfile`](./Dockerfile) - A simple docker image for running the [mongoRepsetBackup.py python script](./mongoRepsetBackup.py) and checking if it works
- [`make-vm-snapshot.sh`](./make-vm-snapshot.sh) - Dummy 'backup script' to test the python [mongoRepsetBackup.py python script](./mongoRepsetBackup.py)

### Helpful Testing Commands

Commands for building and running the test python container:

```bash
# Build the container image
docker build -t mongobackup-python .
# Run the container image inside the replica set network
docker run -it --rm --name testpoint --network mongobackup_mongo-network mongobackup-python 
```

Command for cleaning up the replica set after use:

```bash
docker-compose --file docker-compose-replicaset.yml stop && docker-compose --file docker-compose-replicaset.yml rm -f
```
