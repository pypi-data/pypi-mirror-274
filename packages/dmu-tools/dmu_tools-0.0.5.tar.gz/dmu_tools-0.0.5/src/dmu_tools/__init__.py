from .dmu import TestDay
from .dmu import write_ani_dir

def ANALYSE_TESTDAY(dir_sol:str, dir_lst:str, dir_data:str, id_index:str, start_day:str, end_day:str):
    """
    测定日分析
    :param dir_sol: sol文件路径
    :param dir_lst: lst文件路径
    :param dir_data: data文件路径
    :param id_index: 个体号在data中在第几列
    :param start_day: 开始时间
    :param end_day: 结束时间
    """
    testday = TestDay(dir_sol, dir_lst, dir_data,id_index, start_day, end_day)
    testday.analyse()
    return "TESTDAY"

def GENERATE_TESTDAY():
    return "TESTDAY"

def GENERATE_ANIMAL():
    write_ani_dir()
    return "ANIMAL"