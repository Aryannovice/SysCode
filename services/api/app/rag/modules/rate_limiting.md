# Rate Limiting

Rate limiting controls how frequently clients (e.g. users or services) can make requests to a resource. By setting caps on requests per time unit, systems can prevent abuse and protect backend services from overload. For example, an API gateway might enforce a rule of "100 requests per minute per API key," returning an error or throttling further requests once that limit is reached. This helps defend against attacks (such as DDoS or brute-force login attempts) and ensures fair usage of shared resources. Rate limiting can be implemented client-side, server-side, or by an intermediary (like an API gateway or load balancer), and typically involves keeping counters or using token buckets to track usage.

## Common Use Cases

- **API protection:** Throttling client applications or public APIs to prevent spikes that could overwhelm the server
- **Security:** Guarding against brute-force attacks or credential stuffing by limiting login attempts from the same IP or user
- **Fair usage:** Ensuring that high-traffic clients or bots don't monopolize resources, thus providing predictable performance for all users
- **Automated abuse prevention:** Preventing mass actions such as account creations, email sends, or data scraping by capping rate of those operations
- **Cost control:** In cloud services, rate limiting can cap usage to avoid unexpectedly high bills

## Trade-offs

- **Added latency:** Checking and updating rate-limit counters introduces extra processing per request. A centralized rate-limiting service can add a network hop (10–20ms or more)
- **Complexity:** Implementing distributed rate limits can be complex (especially under high load). Ensuring a consistent count across multiple servers or regions requires careful design
- **False positives/negatives:** If thresholds are set too low, legitimate clients may be blocked (hurting user experience); if too high, abusive traffic might slip through. Tuning limits and windows requires testing and monitoring
- **Single point of failure:** A naive single-node rate limiter can become a bottleneck; high-availability or fail-safe logic (fail-open or fail-closed) must be considered
