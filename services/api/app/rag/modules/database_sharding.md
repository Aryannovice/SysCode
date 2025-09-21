# Database Sharding

Database sharding is a technique for scaling a database by partitioning its data across multiple machines (shards). Instead of storing all data on one server, a shard key (often based on user ID or geographic region) is used to assign each row to one of many database instances. For example, in a user table, users with IDs 1–1,000,000 might go to Shard A, and IDs 1,000,001–2,000,000 to Shard B. Each shard operates independently, so reads and writes for that data happen in parallel on different servers. Sharding enables an application to handle much more data and traffic than a single database server could support.

## Common Use Cases

- **Massive-scale applications:** Any system where data volume and query load grow beyond a single machine's capacity. For example, large social networks or multi-tenant SaaS products often shard their user or tenant data
- **Improving performance:** Distributing rows so that each query touches fewer rows on a given shard, speeding up reads and writes
- **Geographic partitioning:** Placing data closer to users (e.g. North America users on one shard, Europe on another) for latency or compliance reasons
- **Avoiding single point of failure:** With multiple shards, the failure of one machine only affects its slice of data, not the entire database

## Trade-offs

- **Operational complexity:** Managing many database servers is harder than one. Backups, schema changes, and transactions must be handled per-shard. Queries that span shards (joins, aggregations) become complex since they must retrieve and merge results from multiple shards
- **Hotspots:** Some shards may receive much more traffic or store more data than others (if data isn't evenly distributed). This "data hotspot" problem can lead to one shard being overloaded. Choosing a good shard key is critical
- **Increased costs:** More machines means higher infrastructure and maintenance cost. Each shard requires CPU, memory, and storage
- **Application complexity:** The application (or middleware) must know which shard to query. Without built-in sharding support, developers must implement logic to route queries based on the shard key
- **Limited elasticity:** Adding or removing shards often requires rebalancing data, which can be complex and time-consuming
