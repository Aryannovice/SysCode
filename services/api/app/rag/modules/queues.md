# Queues

A queue is a messaging pattern where producers place messages into a queue, and consumers take messages from the queue for processing. Each message is delivered to only one consumer (in contrast to pub/sub where multiple subscribers can get the same message). Queues are often used to decouple parts of a system and to smooth out bursts of work. For example, a web front-end might enqueue tasks (like image processing jobs or email sending) when users submit requests, and worker processes pull tasks from the queue to execute them in the background. This lets the front-end respond quickly (by enqueuing work and returning a response) while the heavier processing happens asynchronously. Common technologies include RabbitMQ, Amazon SQS, and Apache Kafka (when used in queue-like mode).

## Common Use Cases

- **Work queues / background jobs:** Offloading time-consuming tasks (email sending, video encoding, report generation) to be processed asynchronously by worker nodes
- **Load leveling:** Smoothing out spikes by queuing requests during heavy load and processing them at a controlled rate
- **Decoupling services:** Connecting microservices or components so one can produce messages (tasks, events) independently of when another consumes them
- **Retry and resilience:** Queues can hold messages until a consumer is ready or until transient failures are resolved, improving system robustness
- **Task distribution:** Distributing independent tasks (e.g. crawling, data processing) among multiple worker instances to parallelize work

## Trade-offs

- **Eventual consistency:** Queues introduce asynchrony. When a producer writes to the queue, the task is not processed immediately. Readers may see stale state until the queued work is consumed. This favors availability (workers don't block clients) at the expense of immediate consistency
- **Latency:** There can be a delay between message enqueuing and processing, especially under high load or when scaling is triggered
- **Complexity of coordination:** You must manage the queue system, acknowledge messages, handle duplicates, and potentially split/aggregate messages
- **Potential bottlenecks:** If the queue is not distributed or scaled, it can become a single point of failure or congestion
- **Overhead:** Enqueuing and dequeuing messages adds overhead compared to direct calls, though it buys greater decoupling and reliability
