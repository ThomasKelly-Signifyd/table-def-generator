Create table definitions for a Salesforce table based on the types of data in the fields

To Run:

- Open in the IDE of your choice

- pipenv shell

- python table_def_generator.py

NOTE: When the script runs, it will place an unnecessary comma at the end of the file


TABLE_NAME
    e.g. TABLE_NAME = "account.json"
    The name of your table. You must have some sample data for this table so that the script can create a table definition.

SAMPLE_TABLE_DATA_FILENAME:
    e.g. SAMPLE_TABLE_DATA_FILENAME = "{TABLE_NAME}.json"
    This should be rows of the JSON returned from Salesforce using the Salesforce - Redshift ETL
    It is recommended to have 500 to 1000 rows of data so the program can have the best chance of getting the correct column data types
    When you download the JSON from S3 add "[" at the start of the JSON, "," at the end of each line and "]" at the end of the file
    File format should be:
        "[{"id":"0011N000017IjKXQA0"...},{"id":"0011N000017IjKXQA0"...}]"

NEW_TABLE_DEF_FILENAME:
    NEW_TABLE_DEF_FILENAME = "generated_table_defs/{TABLE_NAME}.json"
    The name of the file you want to create. This will use the TABLE_NAME string and be called "{TABLE_NAME}.json"
