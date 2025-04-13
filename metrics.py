from prometheus_client import Counter

http_requests_by_tier = Counter(
    'http_requests_total_by_tier',
    'Total HTTP requests grouped by user tier',
    ['tier']
)
