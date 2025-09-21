# Circuit Breaker

The circuit breaker is a resilience pattern that helps prevent cascading failures in distributed systems. It acts like an electrical circuit breaker: it monitors calls to a remote service, and if failures (exceptions or timeouts) exceed a threshold, it "trips" and stops sending further requests to that service for a period of time. This protects the system from repeatedly trying a failing operation and waiting on timeouts. For example, if Service A calls Service B and Service B becomes unresponsive, a circuit breaker in Service A will quickly open after a few failures, causing further calls to Service B to fail immediately or go to a fallback. Once the error conditions subside, the circuit breaker can allow occasional "test" calls (half-open state) to see if Service B has recovered.

## Common Use Cases

- **Microservice reliability:** Any time one service depends on another (often remote or third-party). A circuit breaker prevents one slow/unresponsive service from tying up threads in calling services
- **External API calls:** Wrapping calls to external systems (payment gateways, email/SMS services) with a circuit breaker to fail fast when the external service is down
- **Fault isolation:** In a batch or stream processing pipeline, preventing a problematic downstream component from stalling the whole pipeline
- **Improving user experience:** Allowing the system to return a default response or degraded functionality quickly when a service is failing, rather than timing out users

## Trade-offs

- **Added complexity:** Implementing circuit breakers requires extra logic to track failure counts, timeouts, and state transitions (closed, open, half-open)
- **Tuning required:** Thresholds and timeouts must be chosen carefully. If thresholds are too low, the circuit may open too often (blocking legitimate traffic); if too high, the breaker may not open in time to protect the system
- **Potential latency on recovery:** Once a circuit opens, users will see immediate failures (or fallbacks) for a time. This can be good (fail fast) but means some requests won't attempt the real operation during the break interval
- **False positives:** Temporary blips can trigger the circuit; careful design (e.g. using sliding windows) is needed to avoid oscillation

