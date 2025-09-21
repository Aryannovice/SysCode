# Consistent Hashing

Consistent hashing is a technique for distributing keys among a changing set of nodes (such as cache servers or shards) with minimal reorganization when nodes join or leave. Imagine a ring where both data keys and nodes are hashed onto the same identifier space. Each key is stored on the nearest clockwise node on the ring. When a node is added or removed, only the keys that map to that node (a small portion of the ring) need to be redistributed, instead of remapping all keys. For example, distributed caches or databases use consistent hashing to assign data (user sessions, cache entries, etc.) to a pool of servers. This way, the system remains balanced even as capacity changes.

## Common Use Cases

- **Distributed caches:** Assigning keys to cache servers (e.g. in a memcached cluster) so that adding/removing a cache server only moves some keys
- **Sharding data stores:** Systems like Amazon DynamoDB, Cassandra, or Riak use consistent hashing to partition data across nodes in a scalable way
- **Load balancing:** Some load balancers use consistent hashing (on IP or request attributes) to route clients consistently to the same server
- **Peer-to-peer systems:** Protocols like Chord use consistent hashing to distribute responsibilities among peers

## Trade-offs

- **Hot spots:** If the hash or data is skewed, some nodes may get much more load than others, causing bottlenecks (Virtual nodes or careful hashing can help mitigate this)
- **Complexity:** Implementing consistent hashing (and maintaining the ring state) is more complex than simple modulo hashing. It often requires extra data structures or coordination
- **Rebalancing:** While much better than a naive rehash, adding or removing nodes still requires moving the subset of keys for that node, which can take time and bandwidth
- **No awareness of node capacity:** Basic consistent hashing treats all nodes equally. If nodes have different capacities, the distribution won't automatically account for that (though virtual nodes can help)
