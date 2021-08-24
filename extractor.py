from rosetta import mean_value
import pandas as pd
import datetime


def prune(measures: list, split_dx_sx: bool = False) -> list:
    pruned_list = []
    pruned_list_dx = []
    pruned_list_sx = []
    for elm in measures:
        if ',' in str(elm):
            elm = str(elm).replace(',', '.')
        if split_dx_sx:
            pruned_list_dx.append(float(elm[:elm.rfind('/')]))
            pruned_list_sx.append(float(elm[elm.rfind('/')+1:]))
        else:
            pruned_list.append(float(elm))
    if split_dx_sx:
        pruned_list.append(pruned_list_dx)
        pruned_list.append(pruned_list_sx)
    return pruned_list

def extract(file: str) -> tuple:
    df = pd.read_excel(file)

    end_column = len(df.columns)
    start_column = 2

    age = int(df.iloc[0][start_column-1])
    height = int(df.iloc[2][start_column-1])
    dom_arm = str(df.iloc[4][start_column-1])

    check_dates = df.iloc[6].to_list()[start_column:end_column]
    check_weight = prune(df.iloc[8].to_list()[start_column:end_column])
    
    check_macro_1 = prune(df.iloc[10].to_list()[start_column:end_column])
    check_macro_2 = prune(df.iloc[11].to_list()[start_column:end_column])
    check_macro_3 = prune(df.iloc[12].to_list()[start_column:end_column])

    check_shoulder = prune(df.iloc[16].to_list()[start_column:end_column])
    check_chest = prune(df.iloc[17].to_list()[start_column:end_column])
    check_arm = prune(df.iloc[18].to_list()[start_column:end_column], split_dx_sx=True)
    check_waist = prune(df.iloc[19].to_list()[start_column:end_column])
    check_leggroin = prune(df.iloc[20].to_list()[start_column:end_column], split_dx_sx=True)
    check_leghalf = prune(df.iloc[21].to_list()[start_column:end_column], split_dx_sx=True)
    check_calf = prune(df.iloc[22].to_list()[start_column:end_column], split_dx_sx=True)
    check_buttock = prune(df.iloc[23].to_list()[start_column:end_column])
    
    check_header = {
        "age": age,
        "height": height,
        "dominant_arm": dom_arm
    }

    check_measurements = {
        "date": check_dates,
        "weight": check_weight,
        "macro1": check_macro_1,
        "macro2": check_macro_2,
        "macro3": check_macro_3,
        "shoulder": check_shoulder,
        "chest": check_chest,
        "arm_dx": check_arm[0],
        "arm_sx": check_arm[1],
        "waist": check_waist,
        "leggroin_dx": check_leggroin[0],
        "leggroin_sx": check_leggroin[1],
        "leghalf_dx": check_leghalf[0],
        "leghalf_sx": check_leghalf[1],
        "calf_dx": check_calf[0],
        "calf_sx": check_calf[1],
        "buttock": check_buttock
    }  

    return (check_header, check_measurements)