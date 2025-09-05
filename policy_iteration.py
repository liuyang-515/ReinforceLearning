import numpy as np


def update_state(s: tuple, a: tuple):
    """return : next state, if_collision_boundary"""
    next_state = (s[0] + a[0], s[1] + a[1])
    if 0 <= next_state[0] <= SIZE - 1 and 0 <= next_state[1] <= SIZE - 1:
        return next_state, False
    return s, True


def cal_sa_return(s: tuple, a: tuple, target_area: list, forbidden_areas: list):
    """s, a, s'"""
    next_state, collison_boundary = update_state(s, a)
    if collison_boundary:
        return -1
    if next_state in forbidden_areas:
        return -10
    elif next_state in target_area:
        return 1
    else:
        return 0


def cal_qsa(s, a, values):
    next_state, _ = update_state(s, a)
    q_a = (
        cal_sa_return(s, a, target_area, forbidden_areas)
        + 0.9 * values[next_state[0], next_state[1]]
    )
    return q_a


# 策略评估
def evaluate_policy(policy):
    values = np.zeros((SIZE, SIZE))
    while True:
        pre_values = values.copy()
        for i in range(SIZE):
            for j in range(SIZE):
                # 每次迭代只更新一次策略
                values[i, j] = cal_qsa((i, j), actions[policy[i, j]], values)
        # 注意：这里是更新完所有的状态之后才进行评估
        if (abs(values - pre_values) < eps).all():
            return values


def show(policy: np.ndarray):
    ans = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    action_shape = {0: ".", 1: "↓", 2: "↑", 3: "→", 4: "←"}
    for i in range(len(policy)):
        for j in range(len(policy[0])):
            ans[i][j] = action_shape[policy[i, j]]
    return ans


# 策略改进
def improve_policy(values):
    policy = np.zeros((SIZE, SIZE), dtype=np.int8)
    for i in range(SIZE):
        for j in range(SIZE):
            max_value_action = -1
            max_value = float("-inf")
            for idx, a in enumerate(actions):
                qsa = cal_qsa((i, j), a, values)
                if qsa > max_value:
                    max_value = qsa
                    max_value_action = idx
            policy[i, j] = max_value_action
    return policy


if __name__ == "__main__":
    SIZE = 5
    actions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    target_area = [(2, 2)]
    forbidden_areas = [(1, 2), (1, 3), (2, 3), (3, 3)]

    gammma = 0.9
    eps = 0.01
    # 策略迭代算法

    # 初始化策略 和 状态值
    policy = np.random.randint(0, 5, (SIZE, SIZE))
    values = np.zeros((SIZE, SIZE))
    # 开始迭代
    while True:
        pre_policy = policy.copy()
        values = evaluate_policy(policy)
        policy = improve_policy(values)
        print("current policy is: ", policy, sep="\n")
        if (pre_policy == policy).all():
            break

    ans = show(policy)
    for i in ans:
        print(i)
    print(values)
