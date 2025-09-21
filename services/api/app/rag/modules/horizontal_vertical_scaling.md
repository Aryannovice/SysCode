# Horizontal and Vertical Scaling

**Vertical scaling** (scaling up) means increasing the power of a single machine – for example, giving it more CPU, RAM, or faster disks. This is simple and can be done by choosing a larger instance type or upgrading hardware. It often works well for databases or applications that can't be easily distributed. The downside is that you hit hardware limits: once you max out the machine's capacity, you cannot scale further. Also, scaling up typically requires downtime (you must restart or replace the server). In contrast, **horizontal scaling** (scaling out) means adding more machines or instances to share the load. For example, instead of one web server, you add three identical servers behind a load balancer. Horizontal scaling offers virtually unlimited capacity (just add more servers) and improves fault tolerance (one machine failing only takes down part of the capacity). However, it requires a distributed architecture (load balancers, distributed caches or databases) and introduces complexity in keeping data consistent across nodes.

## Common Use Cases

- **Vertical:** Upgrading a single database server's RAM/CPU when the DB is maxed out, but can't be sharded easily
- **Horizontal:** Adding more web/API servers behind a load balancer to handle increased traffic; spinning up additional application or worker instances in a cluster
- **Content delivery:** CDNs horizontally scale by adding servers across regions to serve static content

## Trade-offs

- **Vertical scaling:** Easier to implement and maintain (just beef up one machine), but **limited by hardware**. It also has downtime during upgrades and still leaves a single point of failure
- **Horizontal scaling:** Provides much higher capacity and resilience, but **adds complexity**. You need load balancing, distributed storage/cache, and coordination between nodes. Ensuring data consistency across nodes can be challenging and requires orchestration
- **Cost considerations:** Many smaller instances (horizontal) can often be more cost-effective at scale than one huge instance, but the networking and management overhead may increase
