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

## For 2. Design database setup for microservices
**Knowledge Level:** `Novice`
- No professional experience with Databases, other than running queries for developers
- Same thing for Kubernetes, mostly academical experience

### Blog post from Crunchy Data - [The Answer is Postgres; The Question is How?](https://www.crunchydata.com/blog/the-answer-is-postgres-the-question-is-how)

#### Postgres on VMs

> ... **trade-off between the level of effort** to maintain the database **against the flexibility** associated with your choice of **location for deployment** (on-premise, public cloud, etc.).
> 
> ... There are many tools for automating Postgres on VMs, enabling users to reduce the administrative level of effort. Automated or not, you are of course responsible for the database administration.
> 
> Often the choice of **Postgres on VMs is most appropriate when you already have the necessary internal infrastructure and expertise to run databases** and you **want control over both your database and infrastructure** ... In the *public cloud* you may prefer *VM-based Postgres deployments* due to *flexibility in version availability*, *configuration options* and *availability of extensions*.
> 
> In these cases, **Postgres on VMs provides the right balance of flexibility, control and investment**.

#### Postgres on Kubernetes

> ... The **ability to scale up nodes uniformly** makes it **easier to manage hardware** for databases as they grow. Kubernetes features like **node affinity** and **tolerations** allow admins to make decisions about **where Postgres instances are deployed**. These tools combine to **enable database workloads to benefit from high availability** or specific hardware.
> 
> ... Operators and tools such as Helm and Kustomize are all helpful in easing the administrative burden, but **automation and orchestration associated with Kubernetes does not come for free**.
> 
> In the context of Postgres, the question seems to boil down to **whether a user values the benefits of Kubernetes sufficiently to sustain the incremental administration**.

#### Postgres on Managed Services

> ... managed services are an attractive option for deploying databases. ... as **the ‘managed service’ handles a number of the database administration tasks** for you - including **backups**, **patching** and **scaling**.

#### Which one to choose?

> Postgres users **often choose some combination of these deployment models** based upon **their team requirements and organizational standards**. The choice is **less about deciding which model to use for all applications**, and **more about which choice to use for a given project**.
> 
> For many projects, using a **managed service** works well if the use cases require a "**set and forget**" Postgres deployment. The choice between deploying **Postgres on VMs and Kubernetes** is less about a decision for more or less management or automation but rather **based on whether a group is standardizing on Kubernetes**.

![BlogDiagram-1](https://f.hubspotusercontent00.net/hubfs/2283855/BlogDiagram-1.png)

### Blog post from Google Cloud - [To run or not to run a database on Kubernetes: What to consider](https://cloud.google.com/blog/products/databases/to-run-or-not-to-run-a-database-on-kubernetes-what-to-consider)

Options for running databases on [Google Cloud Platform](https://cloud.google.com/) (GCP) and what they’re best used for:

#### Fully managed databases
	
> ... This is the **low-ops choice**, since **Google Cloud handles** many of the maintenance tasks, like **backups**, **patching** and **scaling** ... You just create a database, build your app, and let Google Cloud scale it for you. This **also means you might not have access to the exact version of a database**, **extension**, or the **exact flavor of database** that you want.

#### Do-it-yourself on a VM
	
> ... the **full-ops option**, where you take **full responsibility for building your database**, **scaling it**, **managing reliability**, **setting up backups**, and more. All of that can be a lot of work, **but you have all the features and database flavors** at your disposal.

#### Run it on Kubernetes
	
> ... closer to the **full-ops option**, but you do get **some benefits in terms** of the **automation** Kubernetes provides **to keep the database application running**. That said, it is important to remember that pods (the database application containers) are transient, so **the likelihood of database application restarts or failovers is higher**. Also, **some of the more database-specific administrative tasks**—backups, scaling, tuning, etc.—**are different due** to the added abstractions that come with containerization.

#### Tips for running your database on Kubernetes

>  Since pods are mortal, the likelihood of failover events is higher than a traditionally hosted or fully managed database. It will be **easier to run a database on Kubernetes if it includes concepts like sharding**, **failover elections** and **replication** built into its DNA (for example, ElasticSearch, Cassandra, or MongoDB).

> Some open source projects provide *custom resources* and *operators* to *help with managing the database*.

> Next, *consider the function that database is performing* in the context of your application and business. Databases that are storing **more transient and caching layers are better fits for Kubernetes**. Data layers of that type *typically have more resilience built into the applications, making for a better overall experience*.

> Finally, be sure you **understand the replication modes available** in the database. **Asynchronous modes of replication leave room for data loss**, because *transactions might be committed to the primary database but not to the secondary database(s)*. So, be sure to understand whether you might incur data loss, and how much of that is acceptable in the context of your application.

![https://storage.googleapis.com/gweb-cloudblog-publish/images/Tech_Diag_K8s_Database_Bl.0734067713421317.max-1500x1500.png](https://storage.googleapis.com/gweb-cloudblog-publish/images/Tech_Diag_K8s_Database_Bl.0734067713421317.max-1500x1500.png)

#### How to deploy a database on Kubernetes

> ... With a **StatefulSet**, your **data can be stored on persistent volumes**, decoupling the database application from the persistent storage, so **when a pod** (such as the database application) **is recreated**, **all the data is still there**. Additionally, **when a pod is recreated** in a StatefulSet, **it keeps the same name**, so you have a **consistent endpoint** to connect to. *Persistent data and consistent naming are two of the largest benefits of StatefulSets*. You can check out the Kubernetes [documentation](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) for more details.

> If you need to **run a database that doesn’t perfectly fit the model of a Kubernetes-friendly database** (such as *MySQL* or *PostgreSQL*), consider **using Kubernetes Operators or projects that wrap those database with additional features**. [Operators](https://coreos.com/operators/) will help you spin up those databases and perform database maintenance tasks like backups and replication. For MySQL in particular, take a look at the [Oracle MySQL Operator](https://github.com/oracle/mysql-operator) and [Crunchy Data](https://github.com/CrunchyData/postgres-operator) for PostgreSQL.

> Operators use [custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) and controllers to expose application-specific operations through the Kubernetes API. For example, to perform a backup using Crunchy Data, simply execute `pgo backup [cluster_name]`. To add a Postgres replica, use `pgo scale cluster [cluster_name]`.

> There are some other projects out there that you might explore, such as [Patroni](https://github.com/zalando/patroni) for PostgreSQL. These projects use Operators, but go one step further. They’ve built many tools around their respective databases to aid their operation inside of Kubernetes. They may include additional features like sharding, leader election, and failover functionality needed to successfully deploy MySQL or PostgreSQL in Kubernetes.

### Blog post from RedHat - [Data resiliency for PostgreSQL: Crunchy Data PostgreSQL on Red Hat OpenShift](https://www.redhat.com/en/resources/crunchy-data-postgresql-overview?CrunchyAnonId=ybuarqjrbqqjvryfovjppajpuikguzoojdvvucvmdibawpyr)

Not really super relevant to this topic, but points out the **importance of considering Storage-layer resiliency** (ensuring that the data is persistent and properly stored) in **considering a DB solution**

### Blog post from NetApp - [Azure PostgreSQL: Managed or Self-Managed?](https://bluexp.netapp.com/blog/azure-cvo-blg-azure-postgresql-managed-or-self-managed)

#### Pros and Cons of Fully Managed PostgreSQL in Azure
##### Pros of fully-managed PostgreSQL in Azure

> Fully managed high availability, backup, patching and updates. Most ongoing maintenance efforts are taken care of as part of the managed service.

*Flexible Server*: Scaling resources up and down, and scaling storage up, in the Azure Portal or using the Azure CLI.

> ... *PostgreSQL Hyperscale* (Citrus), ... automatically shard your database and dynamically scale workloads across multiple machines.

> ... storage is an integrated part of the service, and scales automatically based on usage up to 4TB.

##### Cons of fully-managed PostgreSQL in Azure

Azure SQL Database for PostgreSQL **only supports certain PostgreSQL versions**, which *might require upgrading Databases to migrate*

> There is also **no guarantee of the exact DB maintenance time** ... Microsoft advises not to performing long running transactions during the planned maintenance window.

> The DBaaS services are deployed in Azure and can be connected to local data centers in a **hybrid configuration using read replicas**. However, **hybrid deployment is not supported for Flexible Server or Hyperscale** (Citrus).

> ... Database backup is automated, but the schedule and frequency may not always align with your organization’s data protection DR requirements ...

Azure Database for PostgreSQL instances have a hardware cap

> Limit on the number of IOPS supported ...

> Migration between major versions of PostgreSQL is not supported ...

#### Pros and Cons of Self-Managed PostgreSQL in Azure

##### Pros of self-managed PostgreSQL in an Azure VM

Full end-to-end control

> Less expensive than managed options, because you are only paying for compute and storage resources (as well as for the Marketplace image, if you selected a paid option).

> Supports all PostgreSQL versions ...

> You can perform maintenance at any time ...

> Easy to connect your cloud-based database to an on-premises data center.

> Full flexibility to configure schedule and frequency of backups according to your organization’s disaster recovery requirements.

> Ability to use high performance storage services ...

> You can deploy the database on any instance size ...

> No hard limit on the number of IOPS or connections ...

##### Cons of self-managed PostgreSQL in an Azure VM

> When running in an Azure VM, you own the configuration of high availability, backup management, patching, etc. This requires additional effort.

> It is up to you to devise a scaling strategy for compute resources, and configure it using auto scaling features available in Azure VMs ...

> More difficult to manage storage, which relies on Azure managed disks ...

### [Deploy Postgres in Horizontally Scalable Architecture using Kubernetes, Docker, and Kafka on IBM Cloud](https://medium.com/@PankajSinghV/deploy-postgres-in-horizontally-scalable-architecture-using-kubernetes-docker-and-kafka-on-ibm-b29e2ccda26b)
