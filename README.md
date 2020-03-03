Create table definitions for a Salesforce table based on the types of data in the fields

SAMPLE_TABLE_DATA_FILENAME:
    e.g. SAMPLE_TABLE_DATA_FILENAME = "sample_table_data_account.json"
    This should be rows of the JSON returned from Salesforce using the Salesforce - Redshift ETL
    It is recommended to have 500 to 1000 rows of data so the program can have the best chance of getting the correct column data types
    When you download the JSON from S3 add "[" at the start of the JSON, "," at the end of each line and "]" at the end of the file
    File format should be:
        "[{"id":"0011N000017IjKXQA0"...},{"id":"0011N000017IjKXQA0"...}]"

NEW_TABLE_DEF_FILENAME:
    NEW_TABLE_DEF_FILENAME = "generated_table_defs/account.json"
    The name of the file you want to create. This should be called "{table_name}.json"
