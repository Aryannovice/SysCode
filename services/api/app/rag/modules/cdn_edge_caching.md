# CDN and Edge Caching

A Content Delivery Network (CDN) uses globally distributed caches (edge servers) to serve static content closer to users. Edge caching is the general practice of storing frequently accessed data (like images, videos, scripts, API responses) on servers at the "edge" of the network, near end users. When a user requests a cached resource, it is served from a nearby edge server instead of the origin server, drastically reducing latency and backbone traffic. For example, a CDN might cache a website's images in data centers around the world, so users in Europe load images from a European edge cache instead of a distant US server. This improves load times and reduces load on the central server.

## Common Use Cases

- **Static website assets:** Caching images, stylesheets, JavaScript, and other assets on CDN edge nodes for fast delivery
- **Video/audio streaming:** Edge servers or CDNs cache media content so users download from nearby servers, improving streaming performance
- **Large downloads:** Software or update files are cached at CDN endpoints to speed up downloads for a global user base
- **API edge caching:** Caching responses of read-heavy APIs at edge points of presence to reduce origin load (common in global applications)
- **IoT and mobile content:** Pushing data or models to edge caches to reduce latency for devices on constrained networks

## Trade-offs

- **Storage limits and eviction:** Edge caches have finite space, so they must evict older content. Administrators may need to purge or reconfigure caches if they fill up or after updating content
- **Consistency (staleness):** Cached content may become outdated. Ensuring freshness (cache invalidation) requires careful policies (e.g. short TTLs or purge on change)
- **Increased cost:** Deploying and operating edge servers (CDN services or proprietary caches) adds infrastructure cost
- **Complexity:** Edge caching introduces more moving parts. It can be harder to debug issues (since content might come from various caches), and operators have less direct control over exactly where data is stored
- **Reduced control:** In some setups (like third-party CDNs), caching decisions (what stays cached and how long) may be controlled by the CDN rather than by the origin, which can limit flexibility
