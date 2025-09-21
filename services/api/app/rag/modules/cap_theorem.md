# CAP Theorem

The CAP theorem is a principle that applies to distributed systems with networked nodes. It states that in the presence of a network partition (P), a distributed system can provide at most two of the following three guarantees: **Consistency** (all nodes see the same data at the same time) and **Availability** (every request gets a non-error response). In practice, network failures can happen, so systems must tolerate partitions. When a partition occurs, a choice must be made: either sacrifice consistency and serve possibly stale data (favor Availability), or sacrifice availability by rejecting or delaying requests until consistency is restored. This trade-off guides the design of many databases and services (for example, NoSQL systems often choose AP or CP depending on needs).

## Typical Choices

- **CP (Consistency + Partition tolerance):** Guarantees that all nodes will have up-to-date data, but might refuse service (become unavailable) during partitions. Systems like MongoDB or traditional RDBMS clusters often prioritize consistency
- **AP (Availability + Partition tolerance):** Guarantees the system stays online and responsive, but may return stale or diverging data during partitions. Systems like Cassandra or DynamoDB often favor availability, allowing eventual consistency
- **Use-case guidance:** The "best" trade-off depends on application needs. Financial or inventory systems (where accuracy is critical) often lean CP. Global web services (where uptime and low latency matter more) often lean AP

## Trade-offs

- **Consistency vs. Availability:** Under a partition, choosing consistency means some clients may see errors or delays (until data is synchronized), while choosing availability means they might see outdated data
- **Latency:** Ensuring consistency (synchronizing replicas) often adds latency, because responses must wait for multiple nodes to agree
- **Complexity:** Designing around CAP means building in mechanisms for conflict resolution, retries, or recovery after partitions
- **No free lunch:** The CAP theorem highlights that every distributed data system must carefully choose how to balance correctness and resilience; this choice is inherent in the architecture

