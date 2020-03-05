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


def generate_table_defs(table_name):
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
                    no_timestamp += 1
                    data_length = 0
                    break
                elif str(value) != "nan":
                    data_type = "double precision"
                    no_double += 1
                    data_length = 0
                    break
            elif value == True or value == False:
                data_type = "boolean"
                no_bool += 1
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
            no_varchar += 1
        elif data_length < 256:
            data_type = "varchar(256)"
            no_varchar += 1
        elif data_length < 1024:
            data_type = "varchar(1024)"
            no_varchar += 1
        elif data_length < 4096:
            data_type = "varchar(4096)"
            no_varchar += 1
        elif data_length < 8192:
            data_type = "varchar(8192)"
            no_varchar += 1
        else:
            data_type = "varchar(max)"
            no_varchar += 1

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
    for table_name in TABLE_NAMES:
        generate_table_defs(table_name)
