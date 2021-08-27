import pandas as pd
import sys

def prune(measures: list, split_dx_sx: bool = False, int_value: bool = False) -> list:
    pruned_list = []
    pruned_list_dx = []
    pruned_list_sx = []
    
    for elm in measures:
        
        if ',' in str(elm):
            elm = str(elm).replace(',', '.')
        
        if split_dx_sx:
            if elm == '/':
                pruned_list_dx.append(pruned_list_dx[-1])
                pruned_list_sx.append(pruned_list_sx[-1])
            else:
                if int_value:
                    pruned_list_dx.append(int(str(elm)[:str(elm).rfind('/')]))
                    pruned_list_sx.append(int(str(elm)[str(elm).rfind('/')+1:]))
                else:
                    pruned_list_dx.append(float(str(elm)[:str(elm).rfind('/')]))
                    pruned_list_sx.append(float(str(elm)[str(elm).rfind('/')+1:]))
        
        else:
            if elm == '/':
                pruned_list.append(pruned_list[-1])
            else:
                if int_value:
                    pruned_list.append(int(elm))
                else:
                    pruned_list.append(float(elm))

    if split_dx_sx:
        pruned_list.append(pruned_list_dx)
        pruned_list.append(pruned_list_sx)

    return pruned_list

def extract(file: str) -> tuple:
    df = pd.read_excel(file)

    # Automatically detect the number of columns. Thus the number of measurements
    end_column = len(df.columns)
    # Starting column
    start_column = 2
    
    # Parse name
    name = str(df.iloc[0][start_column-1])
    #Parse surname
    surname = str(df.iloc[2][start_column-1])
    # Parse age
    age = int(df.iloc[4][start_column-1])
    # Parse height
    height = int(df.iloc[6][start_column-1])
    # Parse dominant arm
    dom_arm = str(df.iloc[8][start_column-1])
    # Parse data
    check_dates = df.iloc[10].to_list()[start_column:end_column]
    # Parse weight
    check_weight = prune(df.iloc[12].to_list()[start_column:end_column])
    # Parse macros
    check_carbo = prune(df.iloc[14].to_list()[start_column:end_column], split_dx_sx=False, int_value=True)
    check_proteins = prune(df.iloc[15].to_list()[start_column:end_column], split_dx_sx=False, int_value=True)
    check_fat = prune(df.iloc[16].to_list()[start_column:end_column], split_dx_sx=False, int_value=True)
    # Parse circunferences
    check_shoulder = prune(df.iloc[20].to_list()[start_column:end_column])
    check_chest = prune(df.iloc[21].to_list()[start_column:end_column])
    check_arm = prune(df.iloc[22].to_list()[start_column:end_column], split_dx_sx=True)
    check_waist = prune(df.iloc[23].to_list()[start_column:end_column])
    check_leggroin = prune(df.iloc[24].to_list()[start_column:end_column], split_dx_sx=True)
    check_leghalf = prune(df.iloc[25].to_list()[start_column:end_column], split_dx_sx=True)
    check_calf = prune(df.iloc[26].to_list()[start_column:end_column], split_dx_sx=True)
    check_buttock = prune(df.iloc[27].to_list()[start_column:end_column])
    # Parse plicometry
    check_axillary = prune(df.iloc[31].to_list()[start_column:end_column])
    check_pectoral = prune(df.iloc[32].to_list()[start_column:end_column])
    check_side = prune(df.iloc[33].to_list()[start_column:end_column])
    check_scapula = prune(df.iloc[34].to_list()[start_column:end_column])
    check_navel = prune(df.iloc[35].to_list()[start_column:end_column])
    check_triceps = prune(df.iloc[36].to_list()[start_column:end_column])
    check_thigh = prune(df.iloc[37].to_list()[start_column:end_column])

    check_header = {
        "name": name,
        "surname": surname,
        "age": age,
        "height": height,
        "dominant_arm": dom_arm
    }

    check_measurements = {
        "date": check_dates,
        "weight": check_weight,
        "carbo": check_carbo,
        "proteins": check_proteins,
        "fat": check_fat,
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

    check_plicometry = {
        "date": check_dates,
        "axillary": check_axillary,
        "pectoral": check_pectoral,
        "side": check_side,
        "scapula": check_scapula,
        "navel": check_navel,
        "triceps": check_triceps,
        "thich": check_thigh
    }

    return (check_header, check_measurements, check_plicometry)