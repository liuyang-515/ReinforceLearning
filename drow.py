import numpy as np
import matplotlib.pyplot as plt

board_size = 8
chessboard = np.zeros((board_size, board_size))

# 自定义颜色（0: 黑色，1: 红色）
chessboard[::2, ::2] = 1  # 红色格子
chessboard[1::2, 1::2] = 1  # 红色格子

# 定义颜色映射
colors = ["black", "red"]
cmap = plt.cm.colors.ListedColormap(colors)

plt.figure(figsize=(6, 6))
plt.imshow(chessboard, cmap=cmap)
plt.xticks([])
plt.yticks([])
plt.title("Custom Chessboard (Black & Red)")
plt.show()