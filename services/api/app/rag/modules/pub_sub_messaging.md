# Pub/Sub Messaging

Publish/subscribe (pub/sub) is a messaging pattern where senders (publishers) emit messages without knowing who will consume them, and receivers (subscribers) receive messages based on topics or channels they express interest in. The pub/sub broker decouples producers from consumers. For example, an application might publish user activity events ("user login", "item purchased") to a topic, and various services can subscribe to those topics (analytics, logging, notification) to get the events asynchronously. This enables event-driven architectures: one component publishes events and multiple independent subscribers can react to them. Systems like Apache Kafka, RabbitMQ, or cloud messaging services implement pub/sub messaging.

## Common Use Cases

- **Event-driven systems:** Broadcasting events (e.g. user actions, sensor data, system metrics) to multiple downstream services (analytics, audit logs, notifications)
- **Real-time notifications:** Pushing updates (stock changes, chat messages, alerts) to many clients that have subscribed
- **Data streaming:** Streaming log data or telemetry to processing pipelines (e.g. log aggregation, stream processing)
- **Decoupling microservices:** Services communicate by publishing messages rather than calling each other directly, allowing independent scaling and updates
- **Cross-application communication:** Distributing messages from one system to many listeners (e.g. a user-service publishes "profile updated" that triggers caching, email, and auditing services)

## Trade-offs

- **Complexity:** Pub/sub requires a message broker infrastructure and logic to manage topics and subscriptions. Designing for reliability, ordering, and scaling adds complexity compared to point-to-point calls
- **Eventual consistency:** Because messages are delivered asynchronously, subscribers may process events slightly later than when they happened. The system becomes eventually consistent rather than immediately consistent
- **Message loss or duplication:** If the broker or network fails, messages might be lost unless durability or retry mechanisms are in place. Conversely, "at-least-once" delivery can cause duplicates that consumers must deduplicate
- **Ordering:** Ensuring strict order of messages can be difficult, especially when multiple partitions or shards are used. Without special handling, messages may be processed out of order
- **Resource usage:** A high volume of events can load the broker, potentially causing backpressure or latency if not scaled adequately
