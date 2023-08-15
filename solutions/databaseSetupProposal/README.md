# Design database setup for microservices

## Context

> We have two identical environments — test and production — with many services deployed onto k8s clusters. These services need an isolated Postgres database. Developers should have read-write access to all services in test environment and read-only in production.
> 
> The task is to outline a proposal (as a list of key action items and/or a dozen of sentences) on how that could be implemented. We might discuss it deeper in the next interview round.
> 
> Some points to consider:
> - Managed or on-premise
> - Single server or a cluster
> - Single server/cluster, server/cluster per environment or server/cluster per application
> - How to manage and provision accounts for applications and people

## Proposal

