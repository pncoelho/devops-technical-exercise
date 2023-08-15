# Research

## For 1. Consistent Backup Script

**Knowledge Level:** `Novice`
- No professional experience with Databases, other than running queries for developers

### Info from the [MongoDB Manual Intro](https://www.mongodb.com/docs/manual/introduction/)

MongoDB is a **document database**

A **record in MongoDB is a document**, which is a *data structure composed of field and value pairs*. MongoDB **documents are similar to JSON objects**. The values of fields may include other documents, arrays, and arrays of documents.

![A MongoDB document.](https://www.mongodb.com/docs/manual/images/crud-annotated-document.bakedsvg.svg)

The advantages of using documents are:
  - **Documents correspond to native data types** in many programming languages.
  - **Embedded documents and arrays reduce need for expensive joins**.
  - **Dynamic schema supports fluent polymorphism**.

MongoDB **stores documents in** [collections](https://www.mongodb.com/docs/manual/core/databases-and-collections/#std-label-collections). *Collections are analogous to tables* in relational databases.

In addition to collections, MongoDB supports: Read-only [Views](https://www.mongodb.com/docs/manual/core/views/); [On-Demand Materialized Views](https://www.mongodb.com/docs/manual/core/materialized-views/)

MongoDB's replication facility (**high availability**), called [replica set](https://www.mongodb.com/docs/manual/replication/), provides:
- *automatic failover*
- *data redundancy*

A [replica set](https://www.mongodb.com/docs/manual/replication/) is a *group of MongoDB servers* that **maintain the same data set**, providing redundancy and increasing data availability.

MongoDB provides **horizontal scalability** as part of its core functionality:
- [Sharding](https://www.mongodb.com/docs/manual/sharding/#std-label-sharding-introduction) **distributes data across a cluster of machines**.

Starting in 3.4, MongoDB supports creating [zones](https://www.mongodb.com/docs/manual/core/zone-sharding/#std-label-zone-sharding) of data based on the [shard key](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-shard-key). In a balanced cluster, MongoDB directs reads and writes covered by a zone only to those shards inside the zone.

### Info from the [MongoDB ManualDatabases and Collections](https://www.mongodb.com/docs/manual/core/databases-and-collections/)

MongoDB stores data records as [documents](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-document) (specifically [BSON documents](https://www.mongodb.com/docs/manual/core/document/#std-label-bson-document-format)) which are gathered together in [collections](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-collection). A [database](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-database) *stores one or more collections of documents*.

**Document Validation:**

By default, a **collection does not require its documents to have the same schema**; i.e. the documents in a single collection do not need to have the same set of fields and the data type for a field can differ across documents within a collection.

Starting in MongoDB 3.2, however, *you can enforce* [document validation rules](https://www.mongodb.com/docs/manual/core/schema-validation/) *for a collection during update and insert operations*.

**Modifying Document Structure:**

To change the structure of the documents in a collection, such as add new fields, remove existing fields, or change the field values to a new type, **update the documents to the new structure**.

**Unique Identifiers**

**Collections are assigned an immutable UUID**. The *collection UUID remains the same across all members of a replica set and shards in a sharded cluster*.

### Info from the [MongoDB ManualReplication](https://www.mongodb.com/docs/manual/replication/)

A *replica set* in MongoDB is a group of [`mongod`](https://www.mongodb.com/docs/manual/reference/program/mongod/#mongodb-binary-bin.mongod) processes that **maintain the same data set**. Replica sets provide redundancy and [high availability](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-high-availability), and are the basis for all production deployments.

In some cases, replication can provide *increased read capacity* as clients can send read operations to different servers. Maintaining copies of data in different data centers can *increase data locality and availability* for distributed applications. You can also maintain additional copies for dedicated purposes, such as *disaster recovery*, *reporting*, or *backup*.

A replica set contains several data bearing nodes and optionally one arbiter node. Of the data bearing nodes, one and only one member is deemed the primary node, while the other nodes are deemed secondary nodes.

The [primary node](https://www.mongodb.com/docs/manual/core/replica-set-primary/) **receives all write operations**. A replica set can have **only one primary capable of confirming writes** with [`{ w: "majority" }`](https://www.mongodb.com/docs/manual/reference/write-concern/#mongodb-writeconcern-writeconcern.-majority-) write concern;

The **primary records all changes to its data sets in its operation log**, i.e. [oplog](https://www.mongodb.com/docs/manual/core/replica-set-oplog/).

![Diagram of default routing of reads and writes to the primary.](https://www.mongodb.com/docs/manual/images/replica-set-read-write-operations-primary.bakedsvg.svg)

The [secondaries](https://www.mongodb.com/docs/manual/core/replica-set-secondary/) **replicate the primary's oplog** and apply the operations to their data sets such that the secondaries' data sets reflect the primary's data set. If the primary is unavailable, an eligible secondary will hold an election to elect itself the new primary.

![Diagram of a 3 member replica set that consists of a primary and two secondaries.](https://www.mongodb.com/docs/manual/images/replica-set-primary-with-two-secondaries.bakedsvg.svg)

**Secondaries replicate the primary's oplog and apply the operations to their data sets asynchronously.**

By default, clients read from the primary however, clients can specify a [read preference](https://www.mongodb.com/docs/manual/core/read-preference/) to send read operations to secondaries.

### Info from the [MongoDB ManualReplica Set Member](https://www.mongodb.com/docs/manual/core/replica-set-members/)

secondary **maintains a copy of the** [primary's](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-primary) data set. To replicate data, a **secondary applies operations from the primary's** [oplog](https://www.mongodb.com/docs/manual/core/replica-set-oplog/) to its own data set in an **asynchronous process**.

You can configure a secondary member for a specific purpose. You can configure a secondary to:
- Prevent it from becoming a primary in an election, which allows it to reside in a **secondary data center** or to serve as a **cold standby**. See [Priority 0 Replica Set Members.](https://www.mongodb.com/docs/manual/core/replica-set-priority-0-member/)
- Prevent applications from reading from it, which allows it to **run applications that require separation from normal traffic**. See [Hidden Replica Set Members.](https://www.mongodb.com/docs/manual/core/replica-set-hidden-member/)
- Keep a **running "historical" snapshot** for use in **recovery** from certain errors, such as **unintentionally deleted databases**. See [Delayed Replica Set Members.](https://www.mongodb.com/docs/manual/core/replica-set-delayed-member/)

### Info from the [MongoDB ManualReplica Set Oplog](https://www.mongodb.com/docs/manual/core/replica-set-oplog/)

The [oplog](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-oplog) (operations log) is a special [capped collection](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-capped-collection) that **keeps a rolling record of all operations that modify the data stored in your databases**.

Unlike other capped collections, the oplog can grow past its configured size limit to avoid deleting the [`majority commit point`.](https://www.mongodb.com/docs/manual/reference/command/replSetGetStatus/#mongodb-data-replSetGetStatus.optimes.lastCommittedOpTime)

MongoDB 4.4 supports specifying a **minimum oplog retention period in hours**, where MongoDB only removes an oplog entry if:
- The oplog has reached the *maximum configured size*, **and**
- The oplog *entry is older than the configured number of hours*.

MongoDB **applies database operations on the** [primary](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-primary) and then **records the operations on the primary's oplog**. The [secondary](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-secondary) members then **copy and apply these operations in an asynchronous process**. **All replica set members contain a copy of the oplog**, in the [`local.oplog.rs`](https://www.mongodb.com/docs/manual/reference/local-database/#mongodb-data-local.oplog.rs) collection, which allows them to maintain the current state of the database.

To facilitate replication, all replica set members send heartbeats (pings) to all other members. Any [secondary](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-secondary) member can **import oplog entries from any other member**.

Each **operation in the oplog is** [*idempotent*](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-idempotent). That is, oplog operations produce the same results whether applied once or multiple times to the target dataset.

### Info from the [MongoDB ManualBack Up and Restore with Filesystem Snapshots](https://www.mongodb.com/docs/manual/tutorial/backup-with-filesystem-snapshots/)

**Valid Database at the Time of Snapshot**

The *database must be valid when the snapshot takes place*. This means that **all writes accepted by the database need to be fully written to disk**: either to the [journal](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-journal) or to data files.

**If there are writes that are not on disk when the backup occurs, the backup will not reflect these changes**.

**Entire Disk Image**

Snapshots create an image of an entire disk image. Unless you need to back up your entire system, *consider isolating your MongoDB data files, journal* (if applicable), and *configuration on one logical disk that doesn't contain any other data*.

Alternately, store all MongoDB data files on a dedicated device so that you can make backups without duplicating extraneous data.

[Back up Instances with Journal Files on Separate Volume or without Journaling](https://www.mongodb.com/docs/manual/tutorial/backup-with-filesystem-snapshots/#back-up-instances-with-journal-files-on-separate-volume-or-without-journaling)

However, the **database must be locked and all writes to the database must be suspended during the backup process to ensure the consistency of the backup**.

If your [`mongod`](https://www.mongodb.com/docs/manual/reference/program/mongod/#mongodb-binary-bin.mongod) instance is either running without journaling or has the journal files on a separate volume, you **must flush all writes to disk and lock the database to prevent writes during the backup process**. If you have a [replica set](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-replica-set) configuration, then for your backup use a [secondary](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-secondary) which is not receiving reads (i.e. [hidden member](https://www.mongodb.com/docs/manual/reference/glossary/#std-term-hidden-member)).

1. **Flush writes to disk and lock the database to prevent further writes**.
   1. To flush writes to disk and to "lock" the database, issue the [`db.fsyncLock()`](https://www.mongodb.com/docs/manual/reference/method/db.fsyncLock/#mongodb-method-db.fsyncLock) method in [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```
db.fsyncLock();
```

2. **Perform the backup operation**

3. **After the snapshot completes, unlock the database.**
   1. To unlock the database after the snapshot has completed, use the following command in [`mongosh`:](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh)

```
db.fsyncUnlock();
```

### MongoDB connection string info:
- https://www.mongodb.com/docs/manual/reference/connection-string/
- https://www.mongodb.com/docs/mongodb-shell/connect/

### MongoDB Backup recomendations:
- [MongoDb Hot backupcopy data/db VS replicaset with fsyncLock](https://stackoverflow.com/questions/9499674/mongodb-hot-backup-copy-data-db-vs-replicaset-with-fsynclock)
- [Do I need to perform db.fsyncLock() when running a replica set without journal enabled](https://dba.stackexchange.com/questions/203075/do-i-need-to-perform-db-fsynclock-when-running-a-replica-set-without-journal-e)

### PyMongo Tutorials
- https://www.mongodb.com/developer/languages/python/python-quickstart-crud/
- https://www.mongodb.com/languages/python/pymongo-tutorial

### Development and testing environment
- https://www.mongodb.com/compatibility/deploying-a-mongodb-cluster-with-docker
- https://blog.devgenius.io/how-to-deploy-a-mongodb-replicaset-using-docker-compose-a538100db471
