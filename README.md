Create table definitions for a Salesforce table based on the types of data in the fields

To Run:

- Open in the IDE of your choice

- pipenv shell

- python table_def_generator.py


Info:
- Will create a file with JSON schema to create table in Redshift for each table name which is passed into TABLE_NAMES

- Will create a file columns_with_unknown_types which contains any columns where there was no data for the script to guess the datatype. The column names listed in this file are set to varchar(256)


Additional Info:

TABLE_NAMES
    e.g. TABLE_NAMES = ["account.json", "campaign.json",...]
    A list of names of tables. You must have sample data for these tables so that the script can create a table definition for each.

sample_table_data_filename:
    This should be rows of the JSON returned from Salesforce using the Salesforce - Redshift ETL
        NOTE: the sample files included are 10 lines each and are only to show how the file should look
    Download the JSON file for each of these tables from the most recent run IN THE Salesforce bucket on Amazon S3
    When you download the JSON from S3 move the files into the directory sample_table_data/

new_table_def_filename:
    The name of the file you want to create. This will use the table_name string and be called "{table_name}.json"
