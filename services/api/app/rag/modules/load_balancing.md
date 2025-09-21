# Load Balancing

Load balancing distributes incoming traffic or work across multiple servers or resources to optimize performance and avoid overload. By spreading requests evenly, it prevents any single machine from becoming a bottleneck. For example, a load balancer can sit in front of a cluster of web servers and route each client request to one of the healthy servers. This improves overall responsiveness and ensures high availability: if one server fails or is overloaded, the load balancer automatically shifts its share of traffic to the remaining servers. In practice, load balancers use algorithms like round-robin or least-connections to decide where to send each request. They may operate at the network level (layer 4) or application level (layer 7), allowing them to consider IP addresses, URLs, or cookies when balancing. Well-configured load balancing enhances resource utilization, application performance, and fault tolerance.

## Common Use Cases

- Distributing client requests among multiple web or API servers for scaling and redundancy
- Ensuring high availability by routing around failed instances (if a server goes down, its traffic is sent to others)
- Balancing load for microservices or container clusters (e.g. behind a Kubernetes Service)
- Performing rolling upgrades or blue/green deployments by switching traffic between server groups

## Trade-offs

- **Added latency and overhead:** Traffic now passes through the load balancer as an extra network hop, causing slight delays and consuming CPU/memory on the balancer
- **Increased complexity and cost:** Introducing a load balancer adds another component to configure and maintain. For reliability, load balancers themselves often need redundancy (failover), which increases cost
- **Stateful session handling:** Some applications require session affinity; supporting "sticky" sessions or distributed session stores can complicate the design
- **Single point of failure (if unmanaged):** Without a redundant setup, a load balancer can itself become a failure point. (Redundancy and health checks help mitigate this)  
