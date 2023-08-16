# Design Database setup for microservices

## Context

> We have two identical environments — test and production — with many services deployed onto k8s clusters. These services need an isolated Postgres Database. Developers should have read-write access to all services in test environment and read-only in production.
> 
> The task is to outline a proposal (as a list of key action items and/or a dozen of sentences) on how that could be implemented. We might discuss it deeper in the next interview round.
> 
> Some points to consider:
> - Managed or on-premise
> - Single server or a cluster
> - Single server/cluster, server/cluster per environment or server/cluster per application
> - How to manage and provision accounts for applications and people

## Proposal

The first step in proposing any architecture solution is to gather requirements and constraints, so let's look at what information we've been given:
- we have  **two identical k8s environments**
  - *test* and *production*
- that need **isolated Postgres Databases**
- with developers having **read-write access to test** and **read-only to production**.

That's not a lot to start from, but let's look at a few considerations that might help in choosing the correct solution.

### DB Deployment Type

First step is to settle on which type would best suit this scenario. The list of options are:
- **Managed Database service**: where the provider takes care of some DB maintenance tasks and configurations, such as backups and high availability
- **VM DB cluster**: a DB cluster deployed on VMs, either *on-premise* or *Cloud*
- **K8s DB cluster**: a DB cluster deployed on Kubernetes, either *on-premise*, *self-managed on Cloud* or *managed on Cloud*

A few question to help decide on which one to choose:
- Is the **k8s cluster deployed on-premise or on Cloud**?
  - **If on-prem**, then an **on-premise DB cluster** *would likely provide better latency* between the application and the DB
    - Which **would rule out the *managed DB service***
  - **If on Cloud** then a **Cloud DB cluster** *would likely provide better latency* between the application and the DB
    - **Excludes on-premise VM** and **on-premise k8s clusters**
- Are there any **industry specific requirements or standards** (Finacial or Health industries for example) that affect data and it's storage?
  - If so, **Cloud deployment and managed DB service need to be investigated** thoroughly to **ensure they comply** these requirements
  - In some cases, *specific Cloud regions and providers might be required*
  - In others a *full on-premise deployment might be the only option*
- Is there **already existing on-premise infrastructure**?
  - If so, an **on-premise deployment might be a cheaper solution**
- What's the **level of expertise**, *or interest in*, **managing and maintaining DB servers**?
  - If it's **non existing or low**, than a **managed DB service** will most likely your best bet
- **How specific do the Database servers need to be**?
  - If you need old versions of Postgres, specific flavour of Postgres, a lot of compute power and storage, or a lot of fine tunning, then a **managed service will most likely not provide you the flexibility required**
- What's the **level of expertise**, *or interest in*, **managing and maintaining k8s clusters**?
  - If it's **non existing or low**, than a **VM or managed DB service might be better**
  - If it's **high**, running the **Database nodes near the application nodes** in the k8s cluster **might be an improvement in reliability and performance**
    - *Note: this can also be a risk since managing a DB in a k8s is different from a VM environment and requires a good understanding of both k8s and DB management*
- **How agile/fast does the SDLC need to be regarding infrastructure**?
  - If it needs to be **fast**, a **managed DB service** reduces a lot of overhead and allows for fast creation and management of Databases
  - But **if the platform team is using proper IaC and DevOps standards**, *VMs and k8s deployments might be a bit slower*, but **provide a lot more flexibility and a lower cost**

These question are not the only ones you can ask, and more information should be used to consider between them, but it's a good starting point to gather further information.

### DB Architecture

Another important aspect of the Database, which can influence the deployment type and vice-versa, is **how we want to architect our DB**:
- A single server or a cluster?
- How to split up applications and environments?
  - A single server/cluster for all environments and applications?
  - A server/cluster per environment?
  - A server/cluster per application?
  - A server/cluster per environment per application?
- What about high availability, replication, load balancing for example?

There are a lot of different aspect that we could look at, but since the concern in this case is **isolation** between `test` and `prod`, let's have a look at the first two questions, and leave how we setup the Database servers for a later date.

#### Single Server or Cluster?

The answer is simple:
> **Always run clusters for production environments**
> 
> *Can be a VM DB cluster, a DB cluster running inside a k8s cluster, or a managed service DB, or anything else, just ensure you don't have a **single point of failure in terms of Database servers!***

> **For testing run a scaled down version of the production cluster**, whenever possible

While in production we need to be very pragmatic regarding using a cluster, in test we have more flexibility since we have less strict availability and performance requirements, but we still should
- **Ensure the DB is available for testing the actual application**
  - This includes the *DB being available* and *having enough resources for testing*
  - If this *DB cannot meet the minimum availability required for testing the applications*, then **this will delay the SDLC**
- Although we could go for **a single server** (when using either the VM or k8s scenarios), this **is not recommend**
- The *testing environment should be as close to production as possible*, so we should have a *smaller version of our production cluster*, one that is *identical in all aspects except compute and storage*
- This is mainly due to the following reasons:
  - Provides a **more consistent** and *production like* **environment for testing the applications**
  - Allows for **performance testing a scaled down version of the production cluster**
    - This is very helpful for discovering misconfiguration and break points
  - Helps ensure **consistent deployments in production**, since deployment can be tested in the test environment (testing DB deployments using IaC for example)

#### How to separate applications and environments

In this scenario it is stated that *"These services need an **isolated Postgres Database**"*, so let's look at our options and see which ones would fit:
1. **Single DB cluster**
   - Here we would have **separate logical databases** inside the DB cluster, but **both environments** would be **using the same cluster**, which is most likely not what is desired in this scenario, so **let's rule this one out**
2. A **cluster per environment per application**
   - This one would be the solution that provides the **most isolation** and allow for the **most customization of each DB cluster** to each applications needs.
   - But it will be a **more costly solution** and require a **lot more maintenance and administrative load of the DB cluster**, which might not be desired in this scenario.
   - Here the deployment type also plays a big role:
     - If we use a **managed DB service**, then we would **incur bigger costs**, but we would **reduce the maintenance and administrative load** and it would also **facilitate in reporting costs per application**
     - If we used a **VM or k8s cluster scenario**, then we could **potentially decrease the costs**, but it would incur in **high maintenance and administrative load**
   - So this is usually an option when we have a **big company, with a lot of applications and teams and in-house DB and infrastructure (VM or k8s) expertise**
3. **A cluster per environment**
   - This is a **good compromise between isolating** development, testing, quality assurance, production and any other existing **environments** between themselves, **while keeping costs and maintenance and administrative load low**
   - It provides us with confidence that **issues**, whether performance or security related, **in one environment will not affect another one**
   - It's also a *more cost effective scenario that the previous one* (No2), *since we would require only two cluster for the case exposed above, instead of 4*
   - Despite this it still raises the issue that **if a cluster is compromised**, either in a performance or security aspect, **all applications in that environment are compromised**
   - It could also be an issue **if your applications have very different Database requirements** and you need to run them all on the same cluster
4. **A cluster per environment per group of applications**
   - This is the **middle ground between option No2 and option No3**
   - Instead of having a cluster per environment per application, each *application group* would have a cluster per environment
     - For example, if you have 8 applications, divided in to two application groups (`A` & `B`) and you have two environments (`test` and `prod`), you would end up with 4 clusters instead of 16
   - You get a bit of the **advantages of No2**, but try and **keep costs down like No3**
   - *One challenge this scenario poses is that sometimes is not clear how to group application together*

### Conclusion

In the end, with only the information give the only thing we can confidently suggests is:
- Using DB clusters and not single servers
- Using at least one DB cluster per environment, but consider a cluster per environment per group of applications or even a cluster per environment per application

The deployment type (managed, VM or k8s) cannot be suggested since more information would be required and the same thing goes for separating the applications and environments.
