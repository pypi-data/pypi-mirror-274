import pandas as pd
import os
from scipy.stats import pearsonr
from .draw_heritability import draw_heritability as dh


def read_sol(dir_sol):
    sol = pd.read_csv(dir_sol, header=None)[0].str.split(expand=True)
    sol.columns = sol.columns + 1
    return sol


def get_breeding_effects(dir_sol):
    sol = read_sol(dir_sol)
    breeding_effects = sol.loc[sol[1] == "4", :].loc[:, [5, 8]]
    breeding_effects = dict(
        zip(breeding_effects.iloc[:, 0], breeding_effects.iloc[:, 1])
    )
    # 将key转换为int
    breeding_effects = {int(k): float(v) for k, v in breeding_effects.items()}
    return breeding_effects


# 计算遗传力相关
def cal_bv_cor(predict: dict, data: pd.DataFrame, pedigree: pd.DataFrame):
    """计算遗传力相关系数
    Args:
        predict (dict): 预测的个体与表型的对应字典
        data (pd.DataFrame): 原始数据，用来跑动物模型，最后一行为表型
        pedigree (pd.DataFrame): 家系

    Returns:
        float: 相关系数
    """
    # 生成替换数据
    pre_data = get_replace_data(predict, data)
    # 运行
    try:
        pre_bv = cal_bv_ani(predict.keys(), pre_data, pedigree)
        ori_bv = cal_bv_ani(predict.keys(), data, pedigree)
    except:
        print("动物模型运行失败")
        return 0
    # 计算相关系数
    bv_cor = cal_cor(pre_bv, ori_bv)
    print("遗传力相关系数：", bv_cor)
    clean_dmu_files()
    return bv_cor


# 计算相关系数
def cal_cor(pre_bv: dict, ori_bv: dict) -> float:
    # 选取共同的ID
    ids = set(pre_bv.keys()) & set(ori_bv.keys())
    # 选取共同的BV
    pre_bv = {k: pre_bv[k] for k in ids}
    ori_bv = {k: ori_bv[k] for k in ids}
    # 计算相关系数
    bv_cor = pearsonr(list(pre_bv.values()), list(ori_bv.values()))[0]
    return bv_cor


# 生成替换数据
def get_replace_data(predict: dict, data):
    # 生成替换数据
    data = data.copy()
    # 表型，最后一列
    pheno = data.iloc[:, -1].copy()
    # 替换表型
    data["predict"] = data["id"].map(predict)
    data["predict"] = data["predict"].fillna(pheno)
    # 删除phenotype列
    data = data.drop(columns=[pheno.name])
    return data


# 动物模型计算育种值
def cal_bv_ani(target_ids: list, data, pedigree) -> dict:
    # 运行
    run_ani(data, pedigree)
    # 读取结果
    breeding_effects = get_breeding_effects(write_ani_dir() + ".sol")
    # 选取目标
    bv = {k: breeding_effects[k] for k in target_ids}
    return bv


# 跑动物模型
def run_ani(data: pd.DataFrame, pedigree: pd.DataFrame):
    data.to_csv("data.txt", sep=" ", index=False, header=False)
    pedigree.to_csv("ped.txt", sep=" ", index=False, header=False)
    os.system("run_dmuai.bat " + write_ani_dir())


# 测定日模型计算遗传力
def cal_bv_tsd(target_ids: list, data, pedigree) -> pd.DataFrame:
    pass


# 跑测定日模型
def run_tsd(data, pedigree):
    data.to_csv("data.txt", sep=" ", index=False, header=False)
    pedigree.to_csv("ped.txt", sep=" ", index=False, header=False)
    os.system("run_dmuai.bat TSD")


# 删除dmu生成文件
def clean_dmu_files(excepts=[]):
    # 根据后缀删除
    d_drop = [
        ".SOL",
        ".log",
        ".LLIK",
        ".lst",
        ".PAROUT",
        ".RESIDUAL",
        ".PAROUT_STD",
        "data.txt",
        "ped.txt",
    ]
    for except_ in excepts:
        d_drop.remove(except_)
    for root, dirs, files in os.walk("./"):
        for file in files:
            for d in d_drop:
                if file.endswith(d):
                    os.remove(os.path.join(root, file))


# 生成动物模型的DIR文件
def write_ani_dir(DIR="ANI"):
    try:
        os.system.remove(DIR + ".DIR")
    except:
        pass
    COMMENT = "\n"
    ANALYSE = "1 1 0 1"
    DATA = "ASCII (3,1,-999) ./data.txt"
    VARIABLE_1 = "#1    2       3"
    VARIABLE_2 = "BATCH STATION ID"
    VARIABLE_3 = "#1"
    VARIABLE_4 = "PHENO"
    MODEL_1 = "1 1 0 0 0"
    MODEL_2 = "0"
    MODEL_3 = "1 0 3 1 2 3"
    MODEL_4 = "# 1个随机效应（遗传效应）"
    model_5 = "1"
    model_6 = "0"
    model_7 = "0"
    VAR_STR = "1 PED 2 ASCII ./ped.txt"
    RESIDUALS = "ASCII"
    DMUAI_1 = "10"
    DMUAI_2 = "1D-7"
    DMUAI_3 = "1D-6"
    DMUAI_4 = "1"
    DMUAI_5 = "0"
    with open(DIR + ".DIR", "w") as f:
        f.write("$COMMENT\n")
        f.write(COMMENT + "\n")
        f.write("$ANALYSE ")
        f.write(ANALYSE + "\n")
        f.write("$DATA ")
        f.write(DATA + "\n")
        f.write("$VARIABLE\n")
        f.write(VARIABLE_1 + "\n")
        f.write(VARIABLE_2 + "\n")
        f.write(VARIABLE_3 + "\n")
        f.write(VARIABLE_4 + "\n")
        f.write("$MODEL\n")
        f.write(MODEL_1 + "\n")
        f.write(MODEL_2 + "\n")
        f.write(MODEL_3 + "\n")
        f.write(MODEL_4 + "\n")
        f.write(model_5 + "\n")
        f.write(model_6 + "\n")
        f.write(model_7 + "\n")
        f.write("$VAR_STR ")
        f.write(VAR_STR + "\n")
        f.write("$RESIDUALS ")
        f.write(RESIDUALS + "\n")
        f.write("$DMUAI\n")
        f.write(DMUAI_1 + "\n")
        f.write(DMUAI_2 + "\n")
        f.write(DMUAI_3 + "\n")
        f.write(DMUAI_4 + "\n")
        f.write(DMUAI_5 + "\n")
    return DIR


# 计算遗传力
def cal_bv(dir_lst: str) -> float:
    # 读取dir文件
    with open(dir_lst, "r") as f:
        # 出现 FINAL PARAMETERS ESTIMATED 之后
        # 出现 Covariance matrix for random effect no:            1
        pass


# 测定日
import pandas as pd
import numpy as np
import os
from .aic import calculate_AIC
from scipy.stats import pearsonr


class TestDay:
    """测定日sol文件读取器"""

    def __init__(
        self,
        dir_sol: str,
        dir_lst: str,
        dir_data: str,
        id_index: int,
        start_day: int,
        end_day: int,
    ) -> None:
        """
        :param dir_sol: sol文件路径
        :param dir_lst: lst文件路径
        :param dir_data: data文件路径
        :param id_index: 个体号在data中在第几列
        :param start_day: 开始时间
        :param end_day: 结束时间
        """
        self.dir_sol = dir_sol
        self.dir_lst = dir_lst
        self.dir_data = dir_data
        self.id_index = id_index
        self.start_day = start_day
        self.end_day = end_day

        self.sol = self.__read_sol()
        self.data = self.__read_data()
        self.effect_values = []

    def __read_sol(self):
        sol = pd.read_csv(self.dir_sol, header=None)
        # 使用str.split()函数分割数据并扩展成多列
        sol[["1", "2", "阶数", "4", "个体号", "6", "7", "8", "9"]] = sol[0].str.split(
            expand=True
        )
        sol = sol.drop(0, axis=1)
        sol = sol[sol["1"] == "4"]
        return sol

    def __read_data(self):
        data = pd.read_csv(self.dir_data, header=None, sep=" ")
        return data

    def calculate_ebv(self):
        """计算EBV
        :return ebv: dict
        """
        # 每个阶数上每个个体的sol列
        effect_values = {}
        for degree, group in self.sol.groupby("阶数"):
            # 获取该阶数的sol列值并创建DataFrame
            effect_value = group[["个体号", "8"]]
            # 将DataFrame添加到字典中
            effect_values[degree] = effect_value
        ebv = {}
        for id in self.data[self.id_index].unique():
            ebv[id] = 0
        for degree in range(1, self.sol["阶数"].astype(int).max() + 1):
            # 此阶数所有个体各个时间上的log值
            log_value = {}
            for id, group in self.data.groupby(by=self.id_index):
                log_value[id] = list(group[self.id_index + degree])
            # 累加EBV
            for id in self.data[self.id_index].unique():
                effect_value = effect_values[str(degree)]

                effect_value_filtered = effect_value[effect_value["个体号"] == str(id)][
                    "8"
                ]
                if not effect_value_filtered.empty:
                    effect_value = float(effect_value_filtered.iloc[0])
                else:
                    print("The dataframe didn't match the filtering criteria.")
                ebv[id] += (pd.Series(log_value[id]) * effect_value).mean()
                # ebv[id] += effect_value
        # 将ebv转换为DataFrame
        ebv = pd.DataFrame(pd.Series(ebv), columns=["EBV"])
        ebv.index.name = "ID"
        ebv.to_csv("ebv.csv")
        return ebv
    
    def calculate_se(self):
        """
        计算标准误差
        :return: se: dict
        """
        # 每个阶数上每个个体的sol列
        effect_values = {}
        for degree, group in self.sol.groupby("阶数"):
            # 获取该阶数的sol列值并创建DataFrame
            effect_value = group[["个体号", "9"]]
            # 将DataFrame添加到字典中
            effect_values[degree] = effect_value
        ebv = {}
        for id in self.data[self.id_index].unique():
            ebv[id] = 0
        for degree in range(1, self.sol["阶数"].astype(int).max() + 1):
            # 此阶数所有个体各个时间上的log值
            log_value = {}
            for id, group in self.data.groupby(by=self.id_index):
                log_value[id] = list(group[self.id_index + degree])
            # 累加EBV
            for id in self.data[self.id_index].unique():
                effect_value = effect_values[str(degree)]

                effect_value_filtered = effect_value[effect_value["个体号"] == str(id)][
                    "8"
                ]
                if not effect_value_filtered.empty:
                    effect_value = float(effect_value_filtered.iloc[0])
                else:
                    print("The dataframe didn't match the filtering criteria.")
                ebv[id] += (pd.Series(log_value[id]) * effect_value).mean()
                # ebv[id] += effect_value
        # 将ebv转换为DataFrame
        ebv = pd.DataFrame(pd.Series(ebv), columns=["EBV"])
        ebv.index.name = "ID"
        ebv.to_csv("ebv.csv")
        return ebv

    def draw_heritability(self):
        """画遗传力图"""
        dh(self.start_day, self.end_day, self.dir_lst)

    def calculate_AIC(self):
        """计算AIC"""
        return calculate_AIC(self.dir_lst)

    def analyse(self):
        """分析"""
        self.calculate_ebv()
        self.draw_heritability()
        self.calculate_AIC()
        return "TESTDAY"
