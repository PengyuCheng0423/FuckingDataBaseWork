class LinearHash:
    def __init__(self, initial_buckets=8):
        self.buckets = [{} for _ in range(initial_buckets)]
        self.bucket_count = initial_buckets
        self.split_index = 0
        self.threshold = 0.75  # 装填因子阈值

    def _hash(self, key, level=None):
        if level is None:
            level = self.bucket_count
        return hash(key) % level

    def _rehash(self):
        # 当前桶满了，需要分裂
        bucket_to_split = self.buckets[self.split_index]
        new_bucket = {}

        # 将要分裂的桶中的元素重新分配
        for key, value in bucket_to_split.items():
            new_index = self._hash(key, self.bucket_count * 2)
            if new_index < self.bucket_count:
                del self.buckets[new_index][key]
                self.buckets[new_index][key] = value
            else:
                new_bucket[key] = value

        # 更新桶数组
        self.buckets.append(new_bucket)
        self.bucket_count *= 2
        self.split_index += 1
        if self.split_index >= len(self.buckets):
            self.split_index = 0

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        # 如果桶已经存在该键，则更新值
        if key in bucket:
            bucket[key] = value
        else:
            bucket[key] = value
            # 检查是否需要重哈希
            if sum(len(bucket) for bucket in self.buckets) / self.bucket_count > self.threshold:
                self._rehash()

    def retrieve(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        return bucket.get(key, None)

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        if key in bucket:
            del bucket[key]

    def __str__(self):
        return '\n'.join(f'Bucket {i}: {bucket}' for i, bucket in enumerate(self.buckets))

# 示例使用
if __name__ == '__main__':
    lh = LinearHash()
    lh.insert('a', 1)
    lh.insert('b', 2)
    lh.insert('c', 3)
    print(lh.retrieve('a'))  # 输出: 1
    lh.delete('b')
    print(lh.retrieve('b'))  # 输出: None
    print(lh)