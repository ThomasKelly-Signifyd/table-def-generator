import json
import os

import pandas as pd

TABLE_NAMES = [
    "Account",
    "Campaign",
    # "CampaignMember",
    # "Contact",
    # "Lead",
    # "Opportunity",
    # "OpportunityContactRole",
    # "OpportunityHistory",
    # "Task",
    # "User",
]


def generate_table_defs(table_name, list_column_names, list_column_types):
    sample_table_data_filename = f"sample_table_data/{table_name.lower()}.json"

    with open(sample_table_data_filename) as f:
        no_lines = 0
        for line in f:
            no_lines += 1
        print(f"{no_lines} lines in {table_name}\n -- Creating temp file with valid JSON (this could take several minutes)")

    with open(sample_table_data_filename) as f:
        valid_json = "["
        count = 0
        for line in f:
            if count < no_lines-1:
                line = line.replace(line[-1], ",\n")
                valid_json += line
            else:
                valid_json += f"{line}]"
            count += 1

    with open(f"temp_valid_json_{table_name.lower()}.json", "w") as f:
        f.write(valid_json)
            
    with open(f"temp_valid_json_{table_name.lower()}.json") as f:
        data_list = json.loads(valid_json)

    df = pd.DataFrame(data_list)
    df_length = len(df.columns)

    lines = "["

    columns_counted = 0
    for column in df:
        data_type = "unknown"
        data_length = 0

        for value in df[column]:
            if isinstance(value, float):
                if len(str(value)) >= 10 and (
                    "date" in column
                    or "stamp" in column
                    or "time" in column
                    or "since" in column
                    or "_at_" in column
                    or "last_modified" in column
                    or "most_recent" in column
                    or "last_clean_run" in column
                    or "updated" in column
                ):
                    data_type = "timestamp"
                    data_length = 0
                    break
                elif str(value) != "nan":
                    data_type = "double precision"
                    data_length = 0
                    break
            elif column == "firstname" or column == "lastname" or column == "zi_company_name__c":
                data_length = 255
                break
            elif isinstance(value, int) and value not in [0, 1]:
                data_type = "integer"
                data_length = 0
                break
            elif str(value) == "True" or str(value) == "False":
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
                        elif data_type == "varchar(max)":
                            list_column_types[i] = data_type
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
                    elif data_type == "unknown" and list_column_types[i] != "unknown":
                        data_type = list_column_types[i]
                    elif list_column_types[i] == "unknown" and data_type != "unknown":
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


def write_table_defs(table_name, list_column_names, list_column_types, list_unknowns):
    sample_table_data_filename = f"sample_table_data/{table_name.lower()}.json"
    new_table_def_filename = f"generated_table_defs/{table_name.lower()}.json"

    with open(f"temp_valid_json_{table_name.lower()}.json") as f:
        data_list = json.load(f)

    df = pd.DataFrame(data_list)
    df_length = len(df.columns)

    no_varchar = 0
    no_bool = 0
    no_double = 0
    no_timestamp = 0
    no_integer = 0
    no_unknowns = 0
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
                elif data_type == "integer":
                    no_integer += 1
                elif data_type == "unknown":
                    if "date" in column and "_to_date" not in column:
                        data_type = "timestamp"
                        list_column_types[i] = data_type
                        no_timestamp += 1
                    else:
                        data_type = "varchar(256)"
                        list_column_types[i] = data_type
                        no_varchar += 1
                        no_unknowns += 1
                        if column not in list_unknowns:
                            list_unknowns.append(f"{column}\n")
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
        f"\n{total} datatypes set for {table_name}:\n-- {no_varchar} varchars\n-- {no_bool} booleans\n-- {no_timestamp} timestamps\n-- {no_double} doubles\n-- {no_integer} integers"
    )
    if no_unknowns != 0:
        print(f"-- {no_unknowns} unknowns (these have been set to varchar(256))\n\n")
    else:
        print("-- 0 unknowns\n\n") 

    with open(new_table_def_filename, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    list_column_names = []
    list_column_types = []
    list_unknowns = []

    for table_name in TABLE_NAMES:
        generate_table_defs(table_name, list_column_names, list_column_types)

    for table_name in TABLE_NAMES:
        write_table_defs(table_name, list_column_names, list_column_types, list_unknowns)
        os.remove(f"temp_valid_json_{table_name.lower()}.json")

    with open("columns_with_unknown_types.txt", "w") as f:
        f.writelines(list_unknowns)

    print("DONE.\nYou can find the generated table definitions under generated_table_defs/")
