import numpy as np


def update_state(s: tuple, a: tuple):
    """return : next state, if_collision_boundary"""
    next_state = (s[0] + a[0], s[1] + a[1])
    if 0 <= next_state[0] <= SIZE - 1 and 0 <= next_state[1] <= SIZE - 1:
        return next_state, False
    return s, True


def cal_sa_return(s: tuple, a: tuple, target_area: list, forbidden_areas: list):
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


if __name__ == "__main__":
    SIZE = 5
    actions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    target_area = [(2, 2)]
    forbidden_areas = [(1, 2), (1, 3), (2, 3), (3, 3)]

    gammma = 0.9
    eps = 0.001
    # 值迭代，注意：值迭代直接求解的就是贝尔曼最优方程
    # 初始化状态值，
    values = np.zeros((SIZE, SIZE))
    # 更新状态值
    print(values)
    while True:
        # 计算新策略
        pre_values = values.copy()
        for i in range(SIZE):
            for j in range(SIZE):
                max_qa = float("-inf")
                for a in actions:
                    q_sa = cal_qsa((i, j), a, values)
                    max_qa = max(max_qa, q_sa)
                # 更新值
                pre_val = values[i, j]
                values[i, j] = max_qa

        if ((values - pre_values) <= eps).all():
            # 策略
            action_shape = {0: ".", 1: "↓", 2: "↑", 3: "→", 4: "←"}
            # 计算策略，也可以每次更新值的之后顺带更新策略
            stra = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
            for i in range(SIZE):
                for j in range(SIZE):
                    max_val_action = -1
                    max_val = float("-inf")
                    for idx, a in enumerate(actions):
                        q_sa = cal_qsa((i, j), a, values)
                        if q_sa > max_val:
                            max_val = q_sa
                            max_val_action = idx
                    stra[i][j] = action_shape[max_val_action]
            break
    for i in stra:
        print(i)
    print(values)
    # 当前只处理了，如果走路过当前状态，会减少奖励。但是如果位于当前状态，是没有乘法的
