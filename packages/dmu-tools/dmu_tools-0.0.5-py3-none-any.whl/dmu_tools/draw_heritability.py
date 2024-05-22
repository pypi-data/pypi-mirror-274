# 遗传力绘图程序
import re
import numpy as np
from numpy.polynomial import legendre
import pandas as pd
import matplotlib.pyplot as plt

def read_matrices_from_file(filename):
    with open(filename, "r") as file:
        content = file.read()

    start_pos = content.find("FINAL PARAMETERS ESTIMATED")
    end_pos = content.find(
        "Empirical BLUE (E_BLUE) for fixed and BLUP (E_BLUP) for random effects"
    )

    if start_pos != -1:
        content = content[start_pos:end_pos]

    # 寻找所有Covariance matrix for random effect no所在的位置
    start_poses = [
        m.start()
        for m in re.finditer("Covariance matrix for random effect no", content)
    ]
    end_poses = [
        m.start()
        for m in re.finditer("Correlation matrix for random effect no", content)
    ]
    matrices = []
    for start, end in zip(start_poses, end_poses):
        section = content[start:end]
        length = len(list(filter(None, section.split("\n")[2].split(" "))))
        matrix = []
        for i in range(3, length + 3):
            matrix.append(list(filter(None, section.split("\n")[i].split(" ")))[1:])
        matrices.append(matrix)

    start_pos = [m.start() for m in re.finditer("Residual co-variance matrix", content)]

    matrices.append(
        list(filter(None, content[start_pos[0] :].split("\n")[3].split(" ")))[1:]
    )
    # string to float
    return matrices

def get_lg_df(input_data, degree=5):
    lg_df = input_data.copy()[["age", "id"]]
    min_day = lg_df["age"].min()
    max_day = lg_df["age"].max()
    lg_df["standared_day"] = 2 * (lg_df["age"] - min_day) / (max_day - min_day) - 1

    for i in range(degree + 1):
        lg_df['lg' + str(i)] = legendre.legval(lg_df['standared_day'], [0] * i + [1]) * np.sqrt((2 * i + 1) / 2)
    
    return lg_df.drop(["standared_day", "age", "id"], axis=1)

def calculate_var_random(lg_list, matrix):
    var_random = 0
    # 在lg_list开头添加1
    lg_list = [1] + lg_list
    for i in range(len(matrix[-1])):
        for j in range(len(matrix[i])):
            if i == j:
                var_random += float(matrix[i][j]) * (lg_list[i] ** 2)
            else:
                var_random += 2 * float(matrix[i][j]) * lg_list[i] * lg_list[j]
    return var_random

def calculate_heritability(lg_list, matrices):
    var_randoms = []
    for matrix in matrices[:-1]:
        var_randoms.append(calculate_var_random(lg_list, matrix))
    var_residual = float(matrices[-1][0])
    var_total = sum(var_randoms) + var_residual
    return var_randoms[0] / var_total

def draw_heritability(start_day: int, end_day: int, dir_lst: str):
    """绘制遗传力变化图
    :param start_day: 开始时间
    :param end_day: 结束时间
    :param dir_lst: lst文件路径
    """
    lg = pd.DataFrame(
        {
            "id": ["9"] * (end_day - start_day + 1),
            "age": list(range(start_day, end_day + 1)),
        }
    )
    lg = get_lg_df(lg)

    matrices = read_matrices_from_file(dir_lst)
    heritabilities = []
    for i in range(len(lg)):
        heritabilities.append(calculate_heritability(lg.iloc[i, :].values, matrices))
    plt.figure(figsize=(10, 6))
    plt.plot(list(range(start_day, end_day + 1)), heritabilities)
    plt.title("Heritability")
    plt.ylabel("Heritability")
    plt.xlabel("Age")
    plt.show()
