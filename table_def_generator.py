import json

import pandas as pd
import math

SAMPLE_TABLE_DATA_FILENAME = "sample_table_data_account.json"
NEW_TABLE_DEF_FILENAME = "generated_table_defs/account.json"


def main(sample_table_data_filename, new_table_def_filename):
    with open(sample_table_data_filename) as f:
        data_list = json.load(f)

    df = pd.DataFrame(data_list, index=[0])
    df_length = len(df.columns)

    no_varchar = 0
    no_bool = 0
    no_double = 0
    total = 0

    lines = "["
    for column in df:
        # ensure data is not nested.
        # (will be in the dataframe as NaN if so)
        try:
            if math.isnan(df[column].values[0]):
                print(df[column].values[0])
                df_length -= 1
                continue
        except:
            pass
        
        # decide which data type to set the field as
        if df[column].values == None:
            print(f'{{"name" : "{column}", "type" : "varchar(256)"}}')
            lines += f'{{"name" : "{column}", "type" : "varchar(256)"}}'
            no_varchar += 1
        elif isinstance(df[column].values[0], float):
            print(f'{{"name" : "{column}", "type" : "double precision"}}')
            lines += f'{{"name" : "{column}", "type" : "double precision"}}'
            no_double += 1
        elif df[column].values == True or df[column].values == False:
            print(f'{{"name" : "{column}", "type" : "boolean"}}')
            lines += f'{{"name" : "{column}", "type" : "boolean"}}'
            no_bool += 1
        else:
            # decide what lenth of varchar the field should be
            if len(df[column].values[0]) < 256:
                print(f'{{"name" : "{column}", "type" : "varchar(256)"}}')
                lines += f'{{"name" : "{column}", "type" : "varchar(256)"}}'
            elif len(df[column].values[0]) < 1024:
                print(f'{{"name" : "{column}", "type" : "varchar(1024)"}}')
                lines += f'{{"name" : "{column}", "type" : "varchar(1024)"}}'
            elif len(df[column].values[0]) < 8192:
                print(f'{{"name" : "{column}", "type" : "varchar(8192)"}}')
                lines += f'{{"name" : "{column}", "type" : "varchar(8192)"}}'
            else:
                print(f'{{"name" : "{column}", "type" : "varchar(max)"}}')
                lines += f'{{"name" : "{column}", "type" : "varchar(max)"}}'
            no_varchar += 1
        total += 1

        if total != df_length:
            lines += ","

    lines += "]"

    print(
        f"{total} datatypes set:\n-- {no_varchar} varchars\n-- {no_bool} booleans\n-- {no_double} doubles\n\n"
    )

    with open(new_table_def_filename, "w") as f:
        f.writelines(lines)


main(SAMPLE_TABLE_DATA_FILENAME, NEW_TABLE_DEF_FILENAME)
