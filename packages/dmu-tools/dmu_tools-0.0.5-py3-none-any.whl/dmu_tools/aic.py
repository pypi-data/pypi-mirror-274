# AIC计算程序
def get_no_of_paramaters(lst_dir):
    with open(lst_dir, "r") as file:
        content = file.read()

    start_pos = content.find("No. of parameters in Likelihood Function (L)")

    no = list(filter(None, content[start_pos :].split("\n")[0].split(" ")))[-1]
    return int(no)

def get_minustwicelogLikelihood(lst_dir):
    with open(lst_dir, "r") as file:
        content = file.read()
    
    start_pos = content.find("-2LogL")
    value = list(filter(None, content[start_pos :].split("\n")[0].split(" ")))[-3]
    return float(value)

def calculate_AIC(lst_dir):
    no = get_no_of_paramaters(lst_dir)
    value = get_minustwicelogLikelihood(lst_dir)
    print("AIC: ", 2 * no + value)
    return 2 * no + value

# calculate_AIC("AAAAAAA.lst")