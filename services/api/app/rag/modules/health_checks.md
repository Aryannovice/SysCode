# Health Checks

Health checks are periodic tests that verify whether a service instance is functioning properly. Typically, a service exposes a health endpoint (for example, `/health` or `/status`) which returns OK or error based on internal diagnostics (like database connectivity, disk space, or other dependencies). Load balancers, container orchestrators (like Kubernetes), or monitoring systems call these health endpoints. If a service instance reports unhealthy (or fails to respond), it can be removed from the pool of active servers. This ensures that traffic is only sent to instances that are capable of handling requests.

## Common Use Cases

- **Load balancer integration:** The load balancer checks each instance and only forwards traffic to instances whose health check passes
- **Orchestrator probes:** Platforms like Kubernetes use "liveness" and "readiness" probes to restart or halt traffic to pods that fail health checks
- **Self-monitoring:** Services record their own health status (CPU, memory, downstream service connections) to signal when they are under stress and should not receive more work
- **Alerting:** A health check failure can trigger alerts to operators so that issues can be investigated and resolved quickly

## Trade-offs

- **Coverage limitations:** A simple health check might only verify basic uptime or CPU usage. It might not catch all failure modes, and a service could fail between checks
- **Performance overhead:** Checking health frequently adds some load (though typically minimal). Care is needed not to overload the service with too many health requests
- **Flapping and sensitivity:** If health checks are too strict, healthy services might be marked unhealthy during brief spikes (causing unnecessary failovers). If too lenient, genuinely failing services may linger longer before being removed. Tuning the check frequency and timeouts is necessary
