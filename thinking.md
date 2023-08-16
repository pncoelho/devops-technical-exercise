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

## For 2. Design database setup for microservices

### Deployment options:

#### Managed

- *Pros:*
  - **Easiest to maintain**
    - Does not require expertise in managing databases
  - **Easiest to spin up new databases and db cluster**
    - Facilitates prototyping and encourages DevOps practices
  - **Flexible in terms of payment** and makes it **easier to attribute** *Opex* to **teams/projects/departments**
  - **High reliability, backup and data replication out of the box**

- *Cons:*
  - **Least flexible option in terms of the DB itself**
    - May not be viable if using old versions of PostgreSQL or very specific flavors
    - May not be viable due to industry standards (such as data storage, backup or long term storage)
  - **Usually the most expensive option as well**
  - **Does not support fully hybrid cloud solution** (cloud & on-premise clusters)
  - **May cause vendor lock-in**

#### VM Database (*either on-premise or cloud*)

- *Pros:*
  - Traditional and battle tested way of running databases
  - Allows for **full flexibility in terms of database customization, compute power and storage**
  - Can be almost fully automated in terms of deployment and management using modern  IaC and DevOps practices
  - **Low cost option if the infrastructure (and expertise) already exists**

- *Cons:*
  - The **most maintenance and expertise heavy option**
    - Requires expertise on how to properly run databases
    - All DB maintenance tasks need to be performed by the admins
    - All high availability and redundancy concerns need to be implemented by the admins
    - All customization and tweaking needs to be performed by the admins
  - All this **extra maintenance effort** on the DB admins, **might make the overall SDLC slower**

#### Kubernetes (*either on-premise, cloud k8s cluster or managed k8s*)

- *Pros:*
  - Leverage k8s automation and orchestration to **provide higher fault tolerance and high availability**
  - **Database nodes are closer to the application**
  - Allows for the **same flexibility as the VM options**
  - Provides an even **greater standardization of the application**, by containerizing the DB itself

- *Cons:*
  - **Requires** not only a **very good understanding of databases**, but also a **new skill set of performing database maintenance tasks in k8s clusters**
    - backups, scaling, tuning are different due to the added abstractions that come with containerization.
  - **Increases overhead of running a k8s cluster** (specially if is a self-managed cluster, but even for a managed k8s cluster)

### Single server or a cluster

Independent of the deployment, the concern here is the environment:

> **Always run clusters for production environments**
- Can be a VM DB cluster, a DB cluster running inside a k8s cluster, or a managed service DB

For test we have less strict availability and performance requirements, but we still should
- **Ensure the DB is available for testing the actual application**
  - This includes the *DB being available* and *having enough resources for testing*
  - If this *DB cannot meet the minimum availability required for testing the applications*, then **this will delay the SDLC**
- Although we could go for **a single server** (when using either the VM or k8s scenarios), this **is not recommend**
- The *testing environment should be as close to production as possible*, so we should have a *smaller version of our production cluster*, but one that is *identical in all aspects except compute and storage*
- This is mainly due to the following reasons:
  - Provides a **more consistent** and *production like* **environment for testing the applications**
  - Allows for **performance testing a scaled down version of the production cluster**
    - This is very helpful for discovering misconfiguration and break points
  - Helps ensure **consistent deployments in production**, since deployment can be tested in the test environment (testing DB deployments using IaC for example)

> So, **for testing we should run a scaled down version of the production cluster**

### Single server/cluster, server/cluster per environment or server/cluster per application

Let's consider the following options:
1. *Single cluster*
2. *Cluster per environment*
3. *Cluster per application*
4. *Cluster per environment per application*

Here we have 4 factors to consider:
- **Isolation**
  - In terms of isolating the compute power, access and storage, *the preferred choice is №4* and the *worst choice is №1*
  - Options №2 and №3 have different concerns, so let's look at each of them
    - *№2 - Cluster per environment*
      - **Isolating per environment ensures that** compute power, access or storage **issues in the test environment, will not impact production**.
      - However, this does pose two problems:
        - **If the production cluster fails, all databases fail**
        - **If the production cluster is compromised** (in terms of security), **all databases are compromised**
      - If the number of applications that need the database is small, or if there is one primary application and the others are just auxiliary to that one, *then option №2 would be preferred in this scenario*
      - *Usually this is also the most cost effective option* (after №1 of course)
    - *№3 - Cluster per application*
      - This is the **reverse of option №2**, where if one **database cluster fails, only one application is affected**, but there is **no separation from testing and production**
      - This would be *recommended in a scenario where we have multiple application and we want to ensure the highest number of available applications*
- **Flexibility**
  - In terms of flexibility here are our options:
    - *№2 - Cluster per environment*
      - This allows us to have a **test cluster** that is just a **scaled down version of the production one**, but maintaining all of it's important configurations and settings
      - Does make it that *all applications need to run on the same database cluster setup*, which **can be a problem if the applications have very different database requirements** (making this option even impossible in some cases)
    - *№3 - Cluster per application*
      - This allows **each database cluster to be tailor fitted to each application's needs**
      - But we still have the **issue of having the test and production environment in the same database cluster**
    - *№4 - Cluster per environment per application*
      - This has the **upsides of both №2 and №3**, but adds a **big increase in maintenance effort and cost**
- **Maintenance effort**
  - In this case *№1 is the easiest* to manage and *№4 is the hardest* one
  - Regarding options №2 and №3 we have the following concerns
    - If we have a **big number of applications with very different**, or even contradicting database requirements, **than №3 would be the best option**
      - *since №2 could prove very difficult to make every application work with the same DB cluster setup*
    - If we have **applications with similar database requirements**, then running **DB clusters per environment should require less effort** than option №3
    - Also *whichever option requires the least amount of cluster will reduce the amount of effort*
- **Cost**
  - A basic rule of thumb is: *increasing the number of clusters will ensure increasing spending*
    - So *№1 is the least expensive* and *№4 is the most expensive*
  - Between №2 and №3 varies, but I would say *№3 has one advantage*
    - It makes it **easier to know which application has the biggest spending in term of database cluster costs**, since we have cluster per applications

Taking these 4 factors in considerations, the suggestion would be as follows:
- *Cluster per environment per application*
  - **Isolation** (security) **and flexibility are the driving factors**
  - **High level of db management maturity is a requirement**
  - **Cost isn't an inhibiter**
- *Cluster per environment*
  - **Isolation is a concern**
  - **A good level of db management maturity is required**
  - **Provides a cheaper and easier solution to manage than a cluster per environment per application**
- *Groups of clusters separated by environment*
  - Instead of having a cluster per environment, or one cluster per environment per application, we could have **groups of applications that use a set of clusters per environment**
    - Imagine an example with 4 cluster:
    - *Cluster A1* and *B1* would be *production* for *application groups A and B*
    - *Cluster A2* and *B2* would be *testing* for *application groups A and B*
  - Provides **some isolation between application, and full isolation per environment**
  - Is **not as expensive or effort requiring as the cluster per environment per application**

> Being *Cluster per environment* and *Groups of clusters separated by environment* the n1 and n2 most common options, and *Cluster per environment per application* usually reserved for companies with a lot of resources and teams

### How to manage and provision accounts for applications and people

One thing that helps managing users easier is to *use roles to assign permissions to groups whenever possible*, **never managing user permissions individually per user**.

Another aspect that helps is **configuring users, groups, roles and permissions through IaC**, *using some configuration management tool*. This provides the following advantages:
- **Identity management is done and tracked via code**
- **Changes to this code are reviewed, approved and automatically deployed**
- Helps ensure **standardization of identity management**

### Other thoughts

*Specific industry standards or requirements* might make using a **managed database service not viable**.

If the *applications* themselves *are running in k8s clusters*, at least trying and *testing a k8s database deployment is a good idea*, since it might provide: 
- **The application with better resilience and fault tolerance**
- **The team with greater agility**
