from collections import defaultdict

class TimestampBasedConcurrencyControl:
    def __init__(self):
        self.data_items = {}
        self.write_timestamps = {}
        self.read_locks = defaultdict(set)
        self.write_locks = {}
        self.transactions = {}
        self.next_timestamp = 0

    def start_transaction(self, transaction_id):
        self.transactions[transaction_id] = self.next_timestamp
        self.next_timestamp += 1

    def read(self, transaction_id, data_item):
        ts = self.transactions[transaction_id]
        if data_item in self.write_locks and self.write_locks[data_item] != transaction_id:
            print(f"Transaction {transaction_id} aborted due to write lock on {data_item}")
            return None
        if data_item in self.write_timestamps and self.write_timestamps[data_item] >= ts:
            print(f"Transaction {transaction_id} aborted due to write timestamp on {data_item}")
            return None
        self.read_locks[data_item].add(transaction_id)
        return self.data_items.get(data_item, None)

    def write(self, transaction_id, data_item, value):
        ts = self.transactions[transaction_id]
        if data_item in self.write_locks and self.write_locks[data_item] != transaction_id:
            print(f"Transaction {transaction_id} aborted due to write lock on {data_item}")
            return False
        if data_item in self.write_timestamps and self.write_timestamps[data_item] >= ts:
            print(f"Transaction {transaction_id} aborted due to write timestamp on {data_item}")
            return False
        if data_item in self.read_locks and any(t != transaction_id for t in self.read_locks[data_item]):
            print(f"Transaction {transaction_id} aborted due to read lock on {data_item}")
            return False
        self.write_locks[data_item] = transaction_id
        self.data_items[data_item] = value
        self.write_timestamps[data_item] = ts
        return True

    def commit(self, transaction_id):
        for data_item in list(self.read_locks.keys()):
            if transaction_id in self.read_locks[data_item]:
                self.read_locks[data_item].remove(transaction_id)
                if not self.read_locks[data_item]:
                    del self.read_locks[data_item]
        if transaction_id in self.write_locks.values():
            for data_item, tid in list(self.write_locks.items()):
                if tid == transaction_id:
                    del self.write_locks[data_item]
        del self.transactions[transaction_id]
        print(f"Transaction {transaction_id} committed")

    def abort(self, transaction_id):
        for data_item in list(self.read_locks.keys()):
            if transaction_id in self.read_locks[data_item]:
                self.read_locks[data_item].remove(transaction_id)
                if not self.read_locks[data_item]:
                    del self.read_locks[data_item]
        if transaction_id in self.write_locks.values():
            for data_item, tid in list(self.write_locks.items()):
                if tid == transaction_id:
                    del self.write_locks[data_item]
        del self.transactions[transaction_id]
        print(f"Transaction {transaction_id} aborted")

# 示例使用
if __name__ == '__main__':
    tcc = TimestampBasedConcurrencyControl()

    tcc.start_transaction('T1')
    tcc.start_transaction('T2')
    tcc.start_transaction('T3')

    print(tcc.read('T1', 'A'))
    tcc.write('T1', 'A', 10)
    print(tcc.read('T2', 'A')) 
    tcc.write('T2', 'A', 20)
    print(tcc.read('T3', 'A'))
    tcc.write('T3', 'A', 30)
    tcc.commit('T1')
    tcc.abort('T2')
    tcc.abort('T3')