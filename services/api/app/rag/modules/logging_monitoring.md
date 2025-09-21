# Logging and Monitoring

Logging and monitoring are observability practices used to understand and maintain system health. **Logging** records events, errors, and transactions that happen inside an application – for example, user actions, exceptions, or status messages. Log entries are stored (often centrally) so engineers can later search and analyze what happened after the fact. **Monitoring** collects real-time metrics (CPU usage, memory, request rates, error rates) to track system performance continuously. Together, they help teams detect, diagnose, and fix problems. For instance, monitoring might raise an alert when request latency spikes, and logs can then be examined to trace the root cause.

## Common Use Cases

- **Troubleshooting:** Developers and SREs use logs to investigate errors or crashes by examining detailed event history
- **Real-time alerts:** Monitoring systems send alerts when key metrics breach thresholds (e.g. CPU > 80% or error rate > 5%), prompting immediate action
- **Capacity planning:** Monitoring trends (traffic growth, resource usage) guide scaling decisions
- **Auditing and compliance:** Logs provide an audit trail of user actions and system changes, which is important for security and compliance
- **Performance metrics:** Keeping track of application-level metrics (transactions per second, queue depths, etc.) and system-level metrics (disk I/O, network) to ensure SLAs are met

## Trade-offs

- **Overhead and cost:** Collecting logs and metrics consumes disk/network and requires storage (often large volumes of data). High-volume logging and high-resolution monitoring can be expensive
- **Analysis complexity:** Raw logs and metrics are difficult to interpret. Teams need tools (log aggregation, dashboards, APM) and must write queries or set alerts, which takes effort
- **Data volume:** Too much data can lead to alert fatigue. Deciding what to log (error vs. debug) and which metrics to monitor is a balancing act
- **Privacy/security:** Logs may contain sensitive information, so they must be protected. Centralizing logs also creates a valuable target if not secured properly
