class HashTable:
    def __init__(self, hash_size):
        self.n = hash_size
        self.buckets = [[] for _ in range(hash_size)]

    def hash(self, key):
        bucket_no = (key % self.n)
        return bucket_no

    def put(self, key, value):
        bucket_no = self.hash(key)
        self.buckets[bucket_no].append(value)
        # return True

    def get(self, key):
        bucket_no = self.hash(key)
        return self.buckets[bucket_no]

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)

    def display(self):
        for b_no, bucket in enumerate(self.buckets):
            line = "Bucket {}: {}".format(b_no + 1, str(bucket))
            print(line)



