# Caching

Caching stores frequently accessed data closer to where it's needed (often in memory) so that future requests can be served faster. By keeping hot data in a cache, systems can avoid repeating expensive operations like database queries or large file reads. For example, a web application might cache query results in a fast in-memory store (Redis or Memcached) so that repeated page views or API calls return quickly. Caches can exist at multiple levels: in-process, local to each server, or as a shared distributed cache. When designed well, caching greatly improves response time and throughput, and reduces load on back-end systems.

## Common Use Cases

- **Database query caching:** Storing results of common or expensive queries to lighten the load on the database
- **API response caching:** Caching responses from internal or external API calls to reduce redundant work
- **Web content caching (CDNs):** Caching static assets (images, scripts, videos) at content delivery networks or edge servers near users
- **Session and user data:** Keeping session state or user profile data in a fast cache for quick lookups (e.g. session management in Redis)
- **Inter-service caching:** In microservices, caching shared data (like configuration or lookup tables) locally to avoid frequent service calls

## Trade-offs

- **Storage cost:** Caches use fast (often in-memory) storage which is more expensive than regular disk/DB. It's usually not practical to cache the entire dataset
- **Staleness and consistency:** Cached data can become outdated. Updates to the source must invalidate or refresh cache entries, which adds complexity. If not managed, clients may see stale data
- **Cache miss overhead:** When the working set exceeds cache size, lookups fall back to the slower source, possibly causing spikes
- **Distributed cache challenges:** In a multi-server setup, each server's local cache is separate. A load balancer may route a request to a different node that lacks the needed cache entry (This can be mitigated with a shared cache or techniques like consistent hashing)
- **Complexity of invalidation:** Ensuring the cache reflects the source system's state (cache invalidation) is famously tricky and must be handled carefully
