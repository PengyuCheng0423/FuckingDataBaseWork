import random
import threading
import time

class Proposer:
    def __init__(self, proposer_id, acceptors, learners):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.learners = learners
        self.n = 0
        self.value = None
        self.majority = len(acceptors) // 2 + 1

    def propose(self, value):
        self.value = value
        self.n += 1
        self.prepare()

    def prepare(self):
        print(f"Proposer {self.proposer_id} sending prepare({self.n})")
        responses = []
        for acceptor in self.acceptors:
            response = acceptor.receive_prepare(self.n)
            if response:
                responses.append(response)
            if len(responses) >= self.majority:
                break
        if len(responses) >= self.majority:
            self.accept(responses)

    def accept(self, responses):
        max_n = -1
        max_value = None
        for n, value in responses:
            if n > max_n:
                max_n = n
                max_value = value
        value = max_value if max_value is not None else self.value
        print(f"Proposer {self.proposer_id} sending accept({self.n}, {value})")
        responses = []
        for acceptor in self.acceptors:
            response = acceptor.receive_accept(self.n, value)
            if response:
                responses.append(response)
            if len(responses) >= self.majority:
                break
        if len(responses) >= self.majority:
            self.learn(value)

    def learn(self, value):
        print(f"Proposer {self.proposer_id} learned value {value}")
        for learner in self.learners:
            learner.learn(value)

class Acceptor:
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id
        self.promised_n = -1
        self.accepted_n = -1
        self.accepted_value = None

    def receive_prepare(self, n):
        if n > self.promised_n:
            self.promised_n = n
            print(f"Acceptor {self.acceptor_id} promised {n}")
            return (self.accepted_n, self.accepted_value)
        print(f"Acceptor {self.acceptor_id} rejected prepare({n})")
        return None

    def receive_accept(self, n, value):
        if n >= self.promised_n:
            self.accepted_n = n
            self.accepted_value = value
            print(f"Acceptor {self.acceptor_id} accepted ({n}, {value})")
            return True
        print(f"Acceptor {self.acceptor_id} rejected accept({n}, {value})")
        return False

class Learner:
    def __init__(self, learner_id):
        self.learner_id = learner_id

    def learn(self, value):
        print(f"Learner {self.learner_id} learned value {value}")

# 示例使用
if __name__ == '__main__':
    # 创建 Acceptors
    acceptors = [Acceptor(i) for i in range(3)]

    # 创建 Learners
    learners = [Learner(i) for i in range(2)]

    # 创建 Proposers
    proposers = [Proposer(i, acceptors, learners) for i in range(2)]

    # 启动 Proposers
    threads = []
    for proposer in proposers:
        thread = threading.Thread(target=proposer.propose, args=(random.randint(1, 100),))
        threads.append(thread)
        thread.start()

    # 等待所有 Proposers 完成
    for thread in threads:
        thread.join()