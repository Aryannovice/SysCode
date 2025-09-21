# Caching

Caching stores frequently accessed data closer to where it’s needed (often in memory) so that future requests can be served faster.  By keeping hot data in a cache, systems can avoid repeating expensive operations like database queries or large file reads.  For example, a web application might cache query results in a fast in-memory store (Redis or Memcached) so that repeated page views or API calls return quickly.  Caches can exist at multiple levels: in-process, local to each server, or as a shared distributed cache.  When designed well, caching greatly improves response time and throughput, and reduces load on back-end systems:contentReference[oaicite:9]{index=9}.

## Common Use Cases

- **Database query caching:** Storing results of common or expensive queries to lighten the load on the database.  
- **API response caching:** Caching responses from internal or external API calls to reduce redundant work.  
- **Web content caching (CDNs):** Caching static assets (images, scripts, videos) at content delivery networks or edge servers near users.  
- **Session and user data:** Keeping session state or user profile data in a fast cache for quick lookups (e.g. session management in Redis).:contentReference[oaicite:10]{index=10}  
- **Inter-service caching:** In microservices, caching shared data (like configuration or lookup tables) locally to avoid frequent service calls.

## Trade-offs

- **Storage cost:** Caches use fast (often in-memory) storage which is more expensive than regular disk/DB.  It’s usually not practical to cache the entire dataset:contentReference[oaicite:11]{index=11}.  
- **Staleness and consistency:** Cached data can become outdated.  Updates to the source must invalidate or refresh cache entries, which adds complexity.  If not managed, clients may see stale data.  
- **Cache miss overhead:** When the working set exceeds cache size, lookups fall back to the slower source, possibly causing spikes.  
- **Distributed cache challenges:** In a multi-server setup, each server’s local cache is separate.  A load balancer may route a request to a different node that lacks the needed cache entry:contentReference[oaicite:12]{index=12}.  (This can be mitigated with a shared cache or techniques like consistent hashing.)  
- **Complexity of invalidation:** Ensuring the cache reflects the source system’s state (cache invalidation) is famously tricky and must be handled carefully.  

```markdown
# Rate Limiting

Rate limiting controls how frequently clients (e.g. users or services) can make requests to a resource.  By setting caps on requests per time unit, systems can prevent abuse and protect backend services from overload.  For example, an API gateway might enforce a rule of “100 requests per minute per API key,” returning an error or throttling further requests once that limit is reached.  This helps defend against attacks (such as DDoS or brute-force login attempts) and ensures fair usage of shared resources:contentReference[oaicite:13]{index=13}:contentReference[oaicite:14]{index=14}.  Rate limiting can be implemented client-side, server-side, or by an intermediary (like an API gateway or load balancer), and typically involves keeping counters or using token buckets to track usage.

## Common Use Cases

- **API protection:** Throttling client applications or public APIs to prevent spikes that could overwhelm the server:contentReference[oaicite:15]{index=15}.  
- **Security:** Guarding against brute-force attacks or credential stuffing by limiting login attempts from the same IP or user.  
- **Fair usage:** Ensuring that high-traffic clients or bots don’t monopolize resources, thus providing predictable performance for all users:contentReference[oaicite:16]{index=16}.  
- **Automated abuse prevention:** Preventing mass actions such as account creations, email sends, or data scraping by capping rate of those operations.  
- **Cost control:** In cloud services, rate limiting can cap usage to avoid unexpectedly high bills.

## Trade-offs

- **Added latency:** Checking and updating rate-limit counters introduces extra processing per request.  A centralized rate-limiting service can add a network hop (10–20ms or more):contentReference[oaicite:17]{index=17}.  
- **Complexity:** Implementing distributed rate limits can be complex (especially under high load).  Ensuring a consistent count across multiple servers or regions requires careful design.  
- **False positives/negatives:** If thresholds are set too low, legitimate clients may be blocked (hurting user experience); if too high, abusive traffic might slip through.  Tuning limits and windows requires testing and monitoring.  
- **Single point of failure:** A naive single-node rate limiter can become a bottleneck; high-availability or fail-safe logic (fail-open or fail-closed) must be considered:contentReference[oaicite:18]{index=18}.  

```markdown
# Pub/Sub Messaging

Publish/subscribe (pub/sub) is a messaging pattern where senders (publishers) emit messages without knowing who will consume them, and receivers (subscribers) receive messages based on topics or channels they express interest in.  The pub/sub broker decouples producers from consumers. For example, an application might publish user activity events (“user login”, “item purchased”) to a topic, and various services can subscribe to those topics (analytics, logging, notification) to get the events asynchronously.  This enables event-driven architectures: one component publishes events and multiple independent subscribers can react to them.  Systems like Apache Kafka, RabbitMQ, or cloud messaging services implement pub/sub messaging.

## Common Use Cases

- **Event-driven systems:** Broadcasting events (e.g. user actions, sensor data, system metrics) to multiple downstream services (analytics, audit logs, notifications).  
- **Real-time notifications:** Pushing updates (stock changes, chat messages, alerts) to many clients that have subscribed.  
- **Data streaming:** Streaming log data or telemetry to processing pipelines (e.g. log aggregation, stream processing).  
- **Decoupling microservices:** Services communicate by publishing messages rather than calling each other directly, allowing independent scaling and updates.  
- **Cross-application communication:** Distributing messages from one system to many listeners (e.g. a user-service publishes “profile updated” that triggers caching, email, and auditing services).

## Trade-offs

- **Complexity:** Pub/sub requires a message broker infrastructure and logic to manage topics and subscriptions.  Designing for reliability, ordering, and scaling adds complexity compared to point-to-point calls:contentReference[oaicite:19]{index=19}.  
- **Eventual consistency:** Because messages are delivered asynchronously, subscribers may process events slightly later than when they happened.  The system becomes eventually consistent rather than immediately consistent.  
- **Message loss or duplication:** If the broker or network fails, messages might be lost unless durability or retry mechanisms are in place:contentReference[oaicite:20]{index=20}. Conversely, “at-least-once” delivery can cause duplicates that consumers must deduplicate.  
- **Ordering:** Ensuring strict order of messages can be difficult, especially when multiple partitions or shards are used.  Without special handling, messages may be processed out of order:contentReference[oaicite:21]{index=21}.  
- **Resource usage:** A high volume of events can load the broker, potentially causing backpressure or latency if not scaled adequately.

```markdown
# Queues

A queue is a messaging pattern where producers place messages into a queue, and consumers take messages from the queue for processing.  Each message is delivered to only one consumer (in contrast to pub/sub where multiple subscribers can get the same message).  Queues are often used to decouple parts of a system and to smooth out bursts of work. For example, a web front-end might enqueue tasks (like image processing jobs or email sending) when users submit requests, and worker processes pull tasks from the queue to execute them in the background.  This lets the front-end respond quickly (by enqueuing work and returning a response) while the heavier processing happens asynchronously. Common technologies include RabbitMQ, Amazon SQS, and Apache Kafka (when used in queue-like mode).

## Common Use Cases

- **Work queues / background jobs:** Offloading time-consuming tasks (email sending, video encoding, report generation) to be processed asynchronously by worker nodes.  
- **Load leveling:** Smoothing out spikes by queuing requests during heavy load and processing them at a controlled rate.  
- **Decoupling services:** Connecting microservices or components so one can produce messages (tasks, events) independently of when another consumes them.  
- **Retry and resilience:** Queues can hold messages until a consumer is ready or until transient failures are resolved, improving system robustness.  
- **Task distribution:** Distributing independent tasks (e.g. crawling, data processing) among multiple worker instances to parallelize work.  

## Trade-offs

- **Eventual consistency:** Queues introduce asynchrony.  When a producer writes to the queue, the task is not processed immediately.  Readers may see stale state until the queued work is consumed.  This favors availability (workers don’t block clients) at the expense of immediate consistency:contentReference[oaicite:22]{index=22}:contentReference[oaicite:23]{index=23}.  
- **Latency:** There can be a delay between message enqueuing and processing, especially under high load or when scaling is triggered.  
- **Complexity of coordination:** You must manage the queue system, acknowledge messages, handle duplicates, and potentially split/aggregate messages.  
- **Potential bottlenecks:** If the queue is not distributed or scaled, it can become a single point of failure or congestion.  
- **Overhead:** Enqueuing and dequeuing messages adds overhead compared to direct calls, though it buys greater decoupling and reliability.

```markdown
# API Gateway

An API gateway is a server (or service) that acts as a single entry point for a group of microservices or backend services.  Clients (like mobile apps or browsers) send all API requests to the gateway, which then routes each request to the appropriate service.  The gateway can perform cross-cutting tasks on behalf of all services: it can authenticate or authorize requests, aggregate data from multiple services, enforce rate limits, and translate protocols.  For example, a gateway might expose a single `/orderSummary` endpoint: when called, it invokes the user-service and order-service behind the scenes, combines their responses, and returns a unified result to the client:contentReference[oaicite:24]{index=24}.  This simplifies client-side logic and centralizes common functionality.

## Common Use Cases

- **Facade for microservices:** Providing one unified API surface for many backend microservices, so clients need not call each service individually:contentReference[oaicite:25]{index=25}.  
- **Request routing and aggregation:** Routing calls to the correct service and optionally aggregating results from multiple services into one response:contentReference[oaicite:26]{index=26}.  
- **Cross-cutting concerns:** Handling authentication, authorization, logging, metrics, TLS termination, and rate limiting in one place for all APIs.  
- **Protocol translation:** Converting between external protocols (e.g. HTTPS/REST for clients) and internal ones (e.g. gRPC, HTTP on different paths) if needed.  
- **Load balancing:** Some API gateways can distribute calls across instances of a service, acting like a dedicated load balancer.

## Trade-offs

- **Performance overhead:** The gateway adds an extra network hop and work (routing, security, aggregation), which can introduce latency and load on that component:contentReference[oaicite:27]{index=27}.  
- **Single point of failure:** If the gateway goes down (or is not scaled adequately), the entire API layer can become unavailable:contentReference[oaicite:28]{index=28}.  High availability for the gateway itself is critical.  
- **Increased complexity:** Managing and configuring the gateway (routing rules, SSL, auth policies) adds operational complexity:contentReference[oaicite:29]{index=29}.  It essentially becomes another service that must be deployed and maintained.  
- **Tight coupling risk:** If too much business logic or too many responsibilities are shoved into the gateway, it can become bloated and hard to change.  Care must be taken to keep it focused on cross-cutting concerns.  

```markdown
# Database Sharding

Database sharding is a technique for scaling a database by partitioning its data across multiple machines (shards).  Instead of storing all data on one server, a shard key (often based on user ID or geographic region) is used to assign each row to one of many database instances.  For example, in a user table, users with IDs 1–1,000,000 might go to Shard A, and IDs 1,000,001–2,000,000 to Shard B.  Each shard operates independently, so reads and writes for that data happen in parallel on different servers.  Sharding enables an application to handle much more data and traffic than a single database server could support:contentReference[oaicite:30]{index=30}:contentReference[oaicite:31]{index=31}.

## Common Use Cases

- **Massive-scale applications:** Any system where data volume and query load grow beyond a single machine’s capacity.  For example, large social networks or multi-tenant SaaS products often shard their user or tenant data.  
- **Improving performance:** Distributing rows so that each query touches fewer rows on a given shard, speeding up reads and writes:contentReference[oaicite:32]{index=32}.  
- **Geographic partitioning:** Placing data closer to users (e.g. North America users on one shard, Europe on another) for latency or compliance reasons.  
- **Avoiding single point of failure:** With multiple shards, the failure of one machine only affects its slice of data, not the entire database:contentReference[oaicite:33]{index=33}.  

## Trade-offs

- **Operational complexity:** Managing many database servers is harder than one.  Backups, schema changes, and transactions must be handled per-shard.  Queries that span shards (joins, aggregations) become complex since they must retrieve and merge results from multiple shards:contentReference[oaicite:34]{index=34}.  
- **Hotspots:** Some shards may receive much more traffic or store more data than others (if data isn’t evenly distributed).  This “data hotspot” problem can lead to one shard being overloaded:contentReference[oaicite:35]{index=35}.  Choosing a good shard key is critical.  
- **Increased costs:** More machines means higher infrastructure and maintenance cost:contentReference[oaicite:36]{index=36}. Each shard requires CPU, memory, and storage.  
- **Application complexity:** The application (or middleware) must know which shard to query.  Without built-in sharding support, developers must implement logic to route queries based on the shard key:contentReference[oaicite:37]{index=37}.  
- **Limited elasticity:** Adding or removing shards often requires rebalancing data, which can be complex and time-consuming.

```markdown
# CAP Theorem

The CAP theorem is a principle that applies to distributed systems with networked nodes.  It states that in the presence of a network partition (P), a distributed system can provide at most two of the following three guarantees: **Consistency** (all nodes see the same data at the same time) and **Availability** (every request gets a non-error response):contentReference[oaicite:38]{index=38}:contentReference[oaicite:39]{index=39}.  In practice, network failures can happen, so systems must tolerate partitions. When a partition occurs, a choice must be made: either sacrifice consistency and serve possibly stale data (favor Availability), or sacrifice availability by rejecting or delaying requests until consistency is restored:contentReference[oaicite:40]{index=40}. This trade-off guides the design of many databases and services (for example, NoSQL systems often choose AP or CP depending on needs).

## Typical Choices

- **CP (Consistency + Partition tolerance):** Guarantees that all nodes will have up-to-date data, but might refuse service (become unavailable) during partitions. Systems like MongoDB or traditional RDBMS clusters often prioritize consistency.  
- **AP (Availability + Partition tolerance):** Guarantees the system stays online and responsive, but may return stale or diverging data during partitions. Systems like Cassandra or DynamoDB often favor availability, allowing eventual consistency.  
- **Use-case guidance:** The “best” trade-off depends on application needs.  Financial or inventory systems (where accuracy is critical) often lean CP.  Global web services (where uptime and low latency matter more) often lean AP.

## Trade-offs

- **Consistency vs. Availability:** Under a partition, choosing consistency means some clients may see errors or delays (until data is synchronized), while choosing availability means they might see outdated data:contentReference[oaicite:41]{index=41}.  
- **Latency:** Ensuring consistency (synchronizing replicas) often adds latency, because responses must wait for multiple nodes to agree.  
- **Complexity:** Designing around CAP means building in mechanisms for conflict resolution, retries, or recovery after partitions.  
- **No free lunch:** The CAP theorem highlights that every distributed data system must carefully choose how to balance correctness and resilience; this choice is inherent in the architecture.

```markdown
# Circuit Breaker

The circuit breaker is a resilience pattern that helps prevent cascading failures in distributed systems.  It acts like an electrical circuit breaker: it monitors calls to a remote service, and if failures (exceptions or timeouts) exceed a threshold, it “trips” and stops sending further requests to that service for a period of time.  This protects the system from repeatedly trying a failing operation and waiting on timeouts. For example, if Service A calls Service B and Service B becomes unresponsive, a circuit breaker in Service A will quickly open after a few failures, causing further calls to Service B to fail immediately or go to a fallback.  Once the error conditions subside, the circuit breaker can allow occasional “test” calls (half-open state) to see if Service B has recovered:contentReference[oaicite:42]{index=42}:contentReference[oaicite:43]{index=43}.

## Common Use Cases

- **Microservice reliability:** Any time one service depends on another (often remote or third-party).  A circuit breaker prevents one slow/unresponsive service from tying up threads in calling services.  
- **External API calls:** Wrapping calls to external systems (payment gateways, email/SMS services) with a circuit breaker to fail fast when the external service is down.  
- **Fault isolation:** In a batch or stream processing pipeline, preventing a problematic downstream component from stalling the whole pipeline.  
- **Improving user experience:** Allowing the system to return a default response or degraded functionality quickly when a service is failing, rather than timing out users.

## Trade-offs

- **Added complexity:** Implementing circuit breakers requires extra logic to track failure counts, timeouts, and state transitions (closed, open, half-open):contentReference[oaicite:44]{index=44}.  
- **Tuning required:** Thresholds and timeouts must be chosen carefully.  If thresholds are too low, the circuit may open too often (blocking legitimate traffic); if too high, the breaker may not open in time to protect the system:contentReference[oaicite:45]{index=45}.  
- **Potential latency on recovery:** Once a circuit opens, users will see immediate failures (or fallbacks) for a time. This can be good (fail fast) but means some requests won’t attempt the real operation during the break interval.  
- **False positives:** Temporary blips can trigger the circuit; careful design (e.g. using sliding windows) is needed to avoid oscillation.

```markdown
# Health Checks

Health checks are periodic tests that verify whether a service instance is functioning properly.  Typically, a service exposes a health endpoint (for example, `/health` or `/status`) which returns OK or error based on internal diagnostics (like database connectivity, disk space, or other dependencies).  Load balancers, container orchestrators (like Kubernetes), or monitoring systems call these health endpoints.  If a service instance reports unhealthy (or fails to respond), it can be removed from the pool of active servers. This ensures that traffic is only sent to instances that are capable of handling requests:contentReference[oaicite:46]{index=46}:contentReference[oaicite:47]{index=47}.

## Common Use Cases

- **Load balancer integration:** The load balancer checks each instance and only forwards traffic to instances whose health check passes.  
- **Orchestrator probes:** Platforms like Kubernetes use “liveness” and “readiness” probes to restart or halt traffic to pods that fail health checks.  
- **Self-monitoring:** Services record their own health status (CPU, memory, downstream service connections) to signal when they are under stress and should not receive more work.  
- **Alerting:** A health check failure can trigger alerts to operators so that issues can be investigated and resolved quickly.  

## Trade-offs

- **Coverage limitations:** A simple health check might only verify basic uptime or CPU usage.  It might not catch all failure modes, and a service could fail between checks:contentReference[oaicite:48]{index=48}.  
- **Performance overhead:** Checking health frequently adds some load (though typically minimal). Care is needed not to overload the service with too many health requests.  
- **Flapping and sensitivity:** If health checks are too strict, healthy services might be marked unhealthy during brief spikes (causing unnecessary failovers). If too lenient, genuinely failing services may linger longer before being removed. Tuning the check frequency and timeouts is necessary.  

```markdown
# Autoscaling

Autoscaling automatically adjusts the number of running servers or containers in response to load.  In cloud environments, this is usually done by defining policies or metrics (like CPU usage, request count, or custom app metrics).  When load increases beyond a threshold, new instances are launched (“scale out”); when load drops, instances are terminated (“scale in”).  For example, an auto-scaling group might spin up extra web servers when CPU exceeds 70% for several minutes, and shut them down when CPU remains low.  This helps maintain performance during traffic spikes and saves cost during low usage by matching resources to demand:contentReference[oaicite:49]{index=49}:contentReference[oaicite:50]{index=50}.

## Common Use Cases

- **Cloud services:** Websites and APIs that see variable traffic (e.g., daily or seasonal peaks) can use auto-scaling to expand and contract their server pool automatically.  
- **Event-driven load spikes:** E-commerce sites scaling up for shopping holidays, or streaming platforms scaling out for viral content releases:contentReference[oaicite:51]{index=51}.  
- **Cost optimization:** Startups and small businesses use auto-scaling to pay only for what they need, adding capacity only under load:contentReference[oaicite:52]{index=52}.  
- **Container orchestration:** Kubernetes and similar platforms auto-scale pods based on metrics like requests per second or CPU.  

## Trade-offs

- **Configuration complexity:** Setting up auto-scaling requires careful planning. All tiers (web servers, app servers, databases) may need scaling, and dependencies between components must be considered:contentReference[oaicite:53]{index=53}.  
- **Delayed response:** New instances take time to start (boot up and become healthy), so sudden spikes may briefly overwhelm the system before autoscaling catches up:contentReference[oaicite:54]{index=54}.  
- **Over/undershooting:** Choosing the right metrics and thresholds is challenging.  Scale policies tuned poorly can overprovision (waste cost) or underprovision (leading to slowdowns):contentReference[oaicite:55]{index=55}:contentReference[oaicite:56]{index=56}.  
- **Stateful components:** Not all parts of a system can auto-scale easily (e.g., a monolithic database often requires manual vertical scaling).  Design must favor stateless services for effective autoscaling:contentReference[oaicite:57]{index=57}.  

```markdown
# Horizontal and Vertical Scaling

**Vertical scaling** (scaling up) means increasing the power of a single machine – for example, giving it more CPU, RAM, or faster disks.  This is simple and can be done by choosing a larger instance type or upgrading hardware.  It often works well for databases or applications that can’t be easily distributed.  The downside is that you hit hardware limits: once you max out the machine’s capacity, you cannot scale further.  Also, scaling up typically requires downtime (you must restart or replace the server):contentReference[oaicite:58]{index=58}.  In contrast, **horizontal scaling** (scaling out) means adding more machines or instances to share the load. For example, instead of one web server, you add three identical servers behind a load balancer.  Horizontal scaling offers virtually unlimited capacity (just add more servers) and improves fault tolerance (one machine failing only takes down part of the capacity).  However, it requires a distributed architecture (load balancers, distributed caches or databases) and introduces complexity in keeping data consistent across nodes:contentReference[oaicite:59]{index=59}.

## Common Use Cases

- **Vertical:** Upgrading a single database server’s RAM/CPU when the DB is maxed out, but can’t be sharded easily:contentReference[oaicite:60]{index=60}.  
- **Horizontal:** Adding more web/API servers behind a load balancer to handle increased traffic; spinning up additional application or worker instances in a cluster:contentReference[oaicite:61]{index=61}.  
- **Content delivery:** CDNs horizontally scale by adding servers across regions to serve static content.  

## Trade-offs

- **Vertical scaling:** Easier to implement and maintain (just beef up one machine), but **limited by hardware**:contentReference[oaicite:62]{index=62}.  It also has downtime during upgrades and still leaves a single point of failure.  
- **Horizontal scaling:** Provides much higher capacity and resilience, but **adds complexity**:contentReference[oaicite:63]{index=63}.  You need load balancing, distributed storage/cache, and coordination between nodes.  Ensuring data consistency across nodes can be challenging and requires orchestration.  
- **Cost considerations:** Many smaller instances (horizontal) can often be more cost-effective at scale than one huge instance, but the networking and management overhead may increase.  

```markdown
# Logging and Monitoring

Logging and monitoring are observability practices used to understand and maintain system health.  **Logging** records events, errors, and transactions that happen inside an application – for example, user actions, exceptions, or status messages.  Log entries are stored (often centrally) so engineers can later search and analyze what happened after the fact:contentReference[oaicite:64]{index=64}.  **Monitoring** collects real-time metrics (CPU usage, memory, request rates, error rates) to track system performance continuously:contentReference[oaicite:65]{index=65}.  Together, they help teams detect, diagnose, and fix problems.  For instance, monitoring might raise an alert when request latency spikes, and logs can then be examined to trace the root cause.

## Common Use Cases

- **Troubleshooting:** Developers and SREs use logs to investigate errors or crashes by examining detailed event history.  
- **Real-time alerts:** Monitoring systems send alerts when key metrics breach thresholds (e.g. CPU > 80% or error rate > 5%), prompting immediate action.  
- **Capacity planning:** Monitoring trends (traffic growth, resource usage) guide scaling decisions.  
- **Auditing and compliance:** Logs provide an audit trail of user actions and system changes, which is important for security and compliance.  
- **Performance metrics:** Keeping track of application-level metrics (transactions per second, queue depths, etc.) and system-level metrics (disk I/O, network) to ensure SLAs are met.

## Trade-offs

- **Overhead and cost:** Collecting logs and metrics consumes disk/network and requires storage (often large volumes of data).  High-volume logging and high-resolution monitoring can be expensive.  
- **Analysis complexity:** Raw logs and metrics are difficult to interpret.  Teams need tools (log aggregation, dashboards, APM) and must write queries or set alerts, which takes effort.  
- **Data volume:** Too much data can lead to alert fatigue.  Deciding what to log (error vs. debug) and which metrics to monitor is a balancing act.  
- **Privacy/security:** Logs may contain sensitive information, so they must be protected.  Centralizing logs also creates a valuable target if not secured properly.  

```markdown
# Consistent Hashing

Consistent hashing is a technique for distributing keys among a changing set of nodes (such as cache servers or shards) with minimal reorganization when nodes join or leave.  Imagine a ring where both data keys and nodes are hashed onto the same identifier space.  Each key is stored on the nearest clockwise node on the ring.  When a node is added or removed, only the keys that map to that node (a small portion of the ring) need to be redistributed, instead of remapping all keys.  For example, distributed caches or databases use consistent hashing to assign data (user sessions, cache entries, etc.) to a pool of servers.  This way, the system remains balanced even as capacity changes.

## Common Use Cases

- **Distributed caches:** Assigning keys to cache servers (e.g. in a memcached cluster) so that adding/removing a cache server only moves some keys.  
- **Sharding data stores:** Systems like Amazon DynamoDB, Cassandra, or Riak use consistent hashing to partition data across nodes in a scalable way:contentReference[oaicite:66]{index=66}.  
- **Load balancing:** Some load balancers use consistent hashing (on IP or request attributes) to route clients consistently to the same server.  
- **Peer-to-peer systems:** Protocols like Chord use consistent hashing to distribute responsibilities among peers.  

## Trade-offs

- **Hot spots:** If the hash or data is skewed, some nodes may get much more load than others, causing bottlenecks:contentReference[oaicite:67]{index=67}.  (Virtual nodes or careful hashing can help mitigate this.)  
- **Complexity:** Implementing consistent hashing (and maintaining the ring state) is more complex than simple modulo hashing.  It often requires extra data structures or coordination.  
- **Rebalancing:** While much better than a naive rehash, adding or removing nodes still requires moving the subset of keys for that node, which can take time and bandwidth.  
- **No awareness of node capacity:** Basic consistent hashing treats all nodes equally.  If nodes have different capacities, the distribution won’t automatically account for that (though virtual nodes can help).  

```markdown
# CDN and Edge Caching

A Content Delivery Network (CDN) uses globally distributed caches (edge servers) to serve static content closer to users.  Edge caching is the general practice of storing frequently accessed data (like images, videos, scripts, API responses) on servers at the “edge” of the network, near end users.  When a user requests a cached resource, it is served from a nearby edge server instead of the origin server, drastically reducing latency and backbone traffic.  For example, a CDN might cache a website’s images in data centers around the world, so users in Europe load images from a European edge cache instead of a distant US server:contentReference[oaicite:68]{index=68}. This improves load times and reduces load on the central server.

## Common Use Cases

- **Static website assets:** Caching images, stylesheets, JavaScript, and other assets on CDN edge nodes for fast delivery.  
- **Video/audio streaming:** Edge servers or CDNs cache media content so users download from nearby servers, improving streaming performance.  
- **Large downloads:** Software or update files are cached at CDN endpoints to speed up downloads for a global user base.  
- **API edge caching:** Caching responses of read-heavy APIs at edge points of presence to reduce origin load (common in global applications).  
- **IoT and mobile content:** Pushing data or models to edge caches to reduce latency for devices on constrained networks.  

## Trade-offs

- **Storage limits and eviction:** Edge caches have finite space, so they must evict older content.  Administrators may need to purge or reconfigure caches if they fill up or after updating content.  
- **Consistency (staleness):** Cached content may become outdated.  Ensuring freshness (cache invalidation) requires careful policies (e.g. short TTLs or purge on change).  
- **Increased cost:** Deploying and operating edge servers (CDN services or proprietary caches) adds infrastructure cost:contentReference[oaicite:69]{index=69}.  
- **Complexity:** Edge caching introduces more moving parts.  It can be harder to debug issues (since content might come from various caches), and operators have less direct control over exactly where data is stored:contentReference[oaicite:70]{index=70}.  
- **Reduced control:** In some setups (like third-party CDNs), caching decisions (what stays cached and how long) may be controlled by the CDN rather than by the origin, which can limit flexibility.

