Create table definitions for a Salesforce table based on the types of data in the fields

SAMPLE_TABLE_DATA_FILENAME:
    e.g. SAMPLE_TABLE_DATA_FILENAME = "sample_table_data_account.json"
    This should be a single row of JSON returned from Salesforce using the Salesforce - Redshift ETL
    File format should be:
        {"id":"0011N000017IjKXQA0","isdeleted":false,"masterrecordid":null,"name":"Sspess",..."time_fetched_from_salesforce":1582304112.846342802}

NEW_TABLE_DEF_FILENAME:
    NEW_TABLE_DEF_FILENAME = "generated_table_defs/account.json"
    The name of the file you want to create. This should be called "<table name>.json"
