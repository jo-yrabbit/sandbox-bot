import redis


class RedisHandler():

    def __init__(self, logger=None):
        self.redis_client = None
        self.logger = logger


    def get_messages(self, state, limit=2):
        """Get recent messages"""
        key = f"state:{state}:messages"
        # TODO: What does this return? - list?
        return self.redis_client.lrange(key, 0, limit)


    def start(self, redis_host, redis_port, redis_password):
        if self.redis_client:
            self.logger.error('Failed to start a new redis client due to a client already exists')
            return

        try:
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True
            )
        except Exception as e:
            self.logger.error('Failed to start a new redis client - {}', e.args)
        
        self.redis_client = client


    def store_message(self, state, message) -> bool:
        """Store message in redis"""
        key = f"state:{state}:messages"
        try:
            self.redis_client.lpush(key, message)
        except Exception as e:
            raise Exception('Failed to push store message - {}', e.args)
        
        # TODO: Make configurable
        try:
            self.redis_client.ltrim(key, 0, 99)
        except Exception as e:
            raise Exception('Failed to purge messages exceeding capacity (100) - {}', e.args)
