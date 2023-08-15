# DevOps Technical Exercise

This repository serves as a response to a DevOps technical exercise.

## Exercise

The sent [pdf can be found here](./files/devops-technical_task.pdf), but the content is the following:

###  Consistent backups script

Imagine we have a MongoDB cluster consisting of several data nodes running on managed virtual machines in a cloud. We already have a script that creates snapshots of VM disks and takes a hostname as the only parameter:

```$ make-vm-snapshot vm-hostname```

The task is to create a wrapper script around that script to make a consistent (see https://www.mongodb.com/docs/manual/reference/method/db.fsyncLock/ method) snapshot of one of the secondary nodes. The script will be called as follows:

```$ yourscript “mongodb://admin:password@vm-hostname1,vm-hostname2,vm-hostname3/admi n?otherParams”```

Expected deliverable: a script in python, bash or similar

### Design database setup for microservices

We have two identical environments — test and production — with many services deployed onto k8s clusters. These services need an isolated Postgres database. Developers should have read-write access to all services in test environment and read-only in production.

The task is to outline a proposal (as a list of key action items and/or a dozen of sentences) on how that could be implemented. We might discuss it deeper in the next interview round.

Some points to consider:
- Managed or on-premise
- Single server or a cluster
- Single server/cluster, server/cluster per environment or server/cluster per application
- How to manage and provision accounts for applications and people

## Repository Content

The repository has the following content:
- [The sent DevOps technical task](./files/devops-technical_task.pdf)
- [The solutions for each of the exercises](./solutions/)
- [A research/documentation MD file](./research.md)
- [A MD file describing the thought process behind each of the exercises](./thinking.md)
