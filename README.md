Create table definitions for a Salesforce table based on the types of data in the fields

To Run:

- Open in the IDE of your choice

- pipenv shell

- python table_def_generator.py


Info:
- Will create a file with JSON schema to create table in Redshift for each table name which is passed into TABLE_NAMES

- Will create a file columns_with_unknown_types which contains any columns where there was no data for the script to guess the datatype. These are set to varchar(256)


Additional Info:

TABLE_NAMES
    e.g. TABLE_NAMES = ["account.json", "campaign.json",...]
    A list of names of tables. You must have some sample data for these tables so that the script can create a table definition for each.

sample_table_data_filename:
    This should be rows of the JSON returned from Salesforce using the Salesforce - Redshift ETL
    It is recommended to have 1000+ rows of data so the program can have the best chance of getting the correct column data types
        NOTE: the sample files included are 10 lines each and are only to show how the file should look
    When you download the JSON from S3 add "[" at the start of the JSON, "," at the end of each line and "]" at the end of the file
    File format should be:
        "[{"id":"0011N000017IjKXQA0"...},{"id":"0011N000017IjKXQA0"...}]"

new_table_def_filename:
    The name of the file you want to create. This will use the table_name string and be called "{table_name}.json"
