import time


class CacheStore:

    def __init__(self, logger, ttl_seconds=60):
        self.logger = logger
        self.ttl = ttl_seconds
        self.cache = {}

    # ======================================================
    # SET CACHE
    # ======================================================
    def set(self, key, value):

        self.cache[key] = {
            "value": value,
            "time": time.time()
        }

    # ======================================================
    # GET CACHE
    # ======================================================
    def get(self, key):

        if key not in self.cache:
            return None

        item = self.cache[key]

        if time.time() - item["time"] > self.ttl:
            # expired
            del self.cache[key]
            return None

        return item["value"]

    # ======================================================
    # CHECK EXISTENCE
    # ======================================================
    def exists(self, key):

        return self.get(key) is not None

    # ======================================================
    # CLEAR CACHE
    # ======================================================
    def clear(self):

        self.cache = {}

    # ======================================================
    # CLEAN EXPIRED ITEMS
    # ======================================================
    def cleanup(self):

        now = time.time()

        keys_to_delete = []

        for key, item in self.cache.items():

            if now - item["time"] > self.ttl:
                keys_to_delete.append(key)

        for key in keys_to_delete:
            del self.cache[key]

        self.logger.info(f"Cache cleaned: {len(keys_to_delete)} items removed")
