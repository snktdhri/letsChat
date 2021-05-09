import redis
import time

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 1


### Set up Redis client
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset="utf-8", decode_responses=True)

REDIS_KEYS_SEPERATOR = ':'

### Redis helper functions

def exists(key):
    return r.exists(key)

# Redis treats empty sets/lists as non-existent
def is_empty(set_key):
    return not r.exists(set_key)

def get_list_contents(list_key):
    return r.lrange(list_key, 0, -1)

def add_to_list(list_key, value):
    r.rpush(list_key, value)

def add_to_front_of_list(list_key, value):
    r.lpush(list_key, value)

def pop_from_list(list_key):
    return r.lpop(list_key)

def remove_from_list(list_key, value):
    return True if r.lrem(list_key, -1, value) else False