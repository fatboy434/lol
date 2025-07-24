import redis

class SharedState:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value):
        self.r.set(key, value)

    def get(self, key):
        return self.r.get(key)

    def delete(self, key):
        self.r.delete(key)

    def keys(self, pattern='*'):
        return self.r.keys(pattern)
