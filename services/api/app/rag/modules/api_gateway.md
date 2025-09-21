# API Gateway

An API gateway is a server (or service) that acts as a single entry point for a group of microservices or backend services. Clients (like mobile apps or browsers) send all API requests to the gateway, which then routes each request to the appropriate service. The gateway can perform cross-cutting tasks on behalf of all services: it can authenticate or authorize requests, aggregate data from multiple services, enforce rate limits, and translate protocols. For example, a gateway might expose a single `/orderSummary` endpoint: when called, it invokes the user-service and order-service behind the scenes, combines their responses, and returns a unified result to the client. This simplifies client-side logic and centralizes common functionality.

## Common Use Cases

- **Facade for microservices:** Providing one unified API surface for many backend microservices, so clients need not call each service individually
- **Request routing and aggregation:** Routing calls to the correct service and optionally aggregating results from multiple services into one response
- **Cross-cutting concerns:** Handling authentication, authorization, logging, metrics, TLS termination, and rate limiting in one place for all APIs
- **Protocol translation:** Converting between external protocols (e.g. HTTPS/REST for clients) and internal ones (e.g. gRPC, HTTP on different paths) if needed
- **Load balancing:** Some API gateways can distribute calls across instances of a service, acting like a dedicated load balancer

## Trade-offs

- **Performance overhead:** The gateway adds an extra network hop and work (routing, security, aggregation), which can introduce latency and load on that component
- **Single point of failure:** If the gateway goes down (or is not scaled adequately), the entire API layer can become unavailable. High availability for the gateway itself is critical
- **Increased complexity:** Managing and configuring the gateway (routing rules, SSL, auth policies) adds operational complexity. It essentially becomes another service that must be deployed and maintained
- **Tight coupling risk:** If too much business logic or too many responsibilities are shoved into the gateway, it can become bloated and hard to change. Care must be taken to keep it focused on cross-cutting concerns
