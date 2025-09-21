# Autoscaling

Autoscaling automatically adjusts the number of running servers or containers in response to load. In cloud environments, this is usually done by defining policies or metrics (like CPU usage, request count, or custom app metrics). When load increases beyond a threshold, new instances are launched ("scale out"); when load drops, instances are terminated ("scale in"). For example, an auto-scaling group might spin up extra web servers when CPU exceeds 70% for several minutes, and shut them down when CPU remains low. This helps maintain performance during traffic spikes and saves cost during low usage by matching resources to demand.

## Common Use Cases

- **Cloud services:** Websites and APIs that see variable traffic (e.g., daily or seasonal peaks) can use auto-scaling to expand and contract their server pool automatically
- **Event-driven load spikes:** E-commerce sites scaling up for shopping holidays, or streaming platforms scaling out for viral content releases
- **Cost optimization:** Startups and small businesses use auto-scaling to pay only for what they need, adding capacity only under load
- **Container orchestration:** Kubernetes and similar platforms auto-scale pods based on metrics like requests per second or CPU

## Trade-offs

- **Configuration complexity:** Setting up auto-scaling requires careful planning. All tiers (web servers, app servers, databases) may need scaling, and dependencies between components must be considered
- **Delayed response:** New instances take time to start (boot up and become healthy), so sudden spikes may briefly overwhelm the system before autoscaling catches up
- **Over/undershooting:** Choosing the right metrics and thresholds is challenging. Scale policies tuned poorly can overprovision (waste cost) or underprovision (leading to slowdowns)
- **Stateful components:** Not all parts of a system can auto-scale easily (e.g., a monolithic database often requires manual vertical scaling). Design must favor stateless services for effective autoscaling
