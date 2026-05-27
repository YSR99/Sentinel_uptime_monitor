from rq import Worker
from redis import Redis

redis_conn = Redis(
    host="redis",
    port=6379
)

worker = Worker(
    ["default"],
    connection=redis_conn
)

worker.work()