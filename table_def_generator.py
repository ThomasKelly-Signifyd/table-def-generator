import json

import pandas as pd

TABLE_NAMES = [
    "Account",
    "Campaign",
    "CampaignMember",
    "Contact",
    "Lead",
    "Opportunity",
    "OpportunityContactRole",
    "OpportunityHistory",
    "Task",
    "User",
]


def generate_table_defs(table_name, list_column_names, list_column_types):
    sample_table_data_filename = f"sample_table_data/{table_name.lower()}.json"

    with open(sample_table_data_filename) as f:
        data_list = json.load(f)

    df = pd.DataFrame(data_list)
    df_length = len(df.columns)

    lines = "["

    columns_counted = 0
    for column in df:
        data_type = "varchar(20)"
        data_length = 20

        for value in df[column]:
            if isinstance(value, float):
                if len(str(value)) >= 10 and (
                    "date" in column
                    or "stamp" in column
                    or "time" in column
                    or "since" in column
                    or "_at_" in column
                ):
                    data_type = "timestamp"
                    data_length = 0
                    break
                elif str(value) != "nan":
                    data_type = "double precision"
                    data_length = 0
                    break
            elif value == True or value == False:
                data_type = "boolean"
                data_length = 0
                break
            if isinstance(value, dict):
                data_type = "nested json"
                data_length = 0
                break
            else:
                try:
                    if len(value) > data_length:
                        data_length = len(value)
                except:
                    pass

        if data_length == 0:
            pass
        elif data_length <= 20:
            data_type = "varchar(20)"
        elif data_length < 256:
            data_type = "varchar(256)"
        elif data_length < 1024:
            data_type = "varchar(1024)"
        elif data_length < 4096:
            data_type = "varchar(4096)"
        elif data_length < 8192:
            data_type = "varchar(8192)"
        else:
            data_type = "varchar(max)"

        i = 0
        column_in_list = False
        for value in list_column_names:
            if value == column:
                column_in_list = True
                if list_column_types[i] != data_type:
                    if list_column_types[i] == "double precision" and "varchar" in data_type:
                        data_type = "double precision"
                    elif data_type == "double precision" and "varchar" in list_column_types[i]:
                        list_column_types[i] = "double precision"
                    elif "varchar" in list_column_types[i] and "varchar" in data_type:
                        if list_column_types[i] == "varchar(max)":
                            data_type = list_column_types[i]
                        else:
                            listed_length = list_column_types[i].replace("varchar(", "")
                            listed_length = int(listed_length.replace(")", ""))
                            if listed_length < data_length:
                                list_column_types[i] = data_type
                            elif data_length < listed_length:
                                data_type = list_column_types[i]
                    elif list_column_types[i] == "timestamp" and "date" in column:
                        data_type = list_column_types[i]
                    elif data_type == "timestamp" and "date" in column:
                        list_column_types[i] = data_type
                    else:
                        print(f"--- SELECT TYPE FOR {column}:")
                        user_selection = int(input(f"Which is correct? 1.{list_column_types[i]} or 2.{data_type}? "))
                        if user_selection == 1:
                            data_type == list_column_types[i]
                        elif user_selection == 2:
                            list_column_types[i] = data_type
            i += 1
        if column_in_list == False:
            list_column_names.append(column)
            list_column_types.append(data_type)


def write_table_defs(table_name, list_column_names, list_column_types):
    sample_table_data_filename = f"sample_table_data/{table_name.lower()}.json"
    new_table_def_filename = f"generated_table_defs/{table_name.lower()}.json"

    with open(sample_table_data_filename) as f:
        data_list = json.load(f)

    df = pd.DataFrame(data_list)
    df_length = len(df.columns)

    no_varchar = 0
    no_bool = 0
    no_double = 0
    no_timestamp = 0
    total = 0

    lines = "["

    columns_counted = 0
    for column in df:
        i = 0
        for value in list_column_names:
            if value == column:
                data_type = list_column_types[i]
                if data_type == "double precision":
                    no_double += 1
                elif "varchar" in data_type:
                    no_varchar += 1
                elif data_type == "timestamp":
                    no_timestamp += 1
                elif data_type == "boolean":
                    no_bool += 1
            i += 1
                
        columns_counted += 1
        print(f"{column} --> {data_type}")
        if data_type != "nested json":
            lines += f'{{"name" : "{column}", "type" : "{data_type}"}}'
            if columns_counted < df_length:
                lines += ","
            total += 1

    lines += "]"

    print(
        f"\n{total} datatypes set for {table_name}:\n-- {no_varchar} varchars\n-- {no_bool} booleans\n-- {no_timestamp} timestamps\n-- {no_double} doubles\n\n"
    )

    with open(new_table_def_filename, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    list_column_names = []
    list_column_types = []

    for table_name in TABLE_NAMES:
        generate_table_defs(table_name, list_column_names, list_column_types)

    for table_name in TABLE_NAMES:
        write_table_defs(table_name, list_column_names, list_column_types)
