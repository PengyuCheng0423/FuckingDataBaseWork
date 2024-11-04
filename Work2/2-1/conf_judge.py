from collections import defaultdict, deque

def build_conflict_graph(schedule):
    # 构建冲突图
    conflict_graph = defaultdict(set)
    operations = []

    # 解析调度
    for operation in schedule:
        action, transaction, item = operation
        operations.append((action, transaction, item))

    # 记录每个事务对每个数据项的最后一次操作
    last_operations = defaultdict(lambda: defaultdict(tuple))

    for idx, (action, transaction, item) in enumerate(operations):
        if action == 'W':
            # 写操作
            if item in last_operations:
                for t, op_idx in last_operations[item].items():
                    if t != transaction:
                        conflict_graph[t].add(transaction)
                        conflict_graph[transaction].add(t)
            last_operations[item][transaction] = (action, idx)
        elif action == 'R':
            # 读操作
            if item in last_operations:
                for t, (last_action, op_idx) in last_operations[item].items():
                    if t != transaction and last_action == 'W':
                        conflict_graph[t].add(transaction)
                        conflict_graph[transaction].add(t)
            last_operations[item][transaction] = (action, idx)

    return conflict_graph

def is_cyclic(conflict_graph):
    # 检测冲突图中是否存在环
    visited = set()
    recursion_stack = set()

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in conflict_graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True

        recursion_stack.remove(node)
        return False

    for node in conflict_graph:
        if node not in visited:
            if dfs(node):
                return True

    return False

def is_conflict_serializable(schedule):
    conflict_graph = build_conflict_graph(schedule)
    return not is_cyclic(conflict_graph)

# 示例使用
if __name__ == '__main__':
    schedule = [
        ('R', 'T1', 'B'),
        ('W', 'T1', 'B'),
        ('R', 'T2', 'A'),
        ('W', 'T2', 'B'),
        ('R', 'T3', 'B'),
        ('W', 'T3', 'A')
    ]
    
    print(schedule)
    if is_conflict_serializable(schedule):
        print("The schedule is conflict serializable.")
    else:
        print("The schedule is not conflict serializable.")