-- Create or replace database
CREATE OR REPLACE DATABASE BLOB;

-- Create or replace stage with NEW SAS token
CREATE OR REPLACE STAGE azure_stage
  URL='azure://blobconnect.blob.core.windows.net/saleslive'
  CREDENTIALS=(
    AZURE_SAS_TOKEN='?sv=2024-11-04&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-10-22T12:30:42Z&st=2025-10-15T04:15:42Z&spr=https&sig=ui%2Bl4iiv5ZUiWYaiFuh7guT5XzetieXn2RdlwQWsLUc%3D'
  );

-- Verify stage and list files
LIST @azure_stage;

-- Create or replace destination table
CREATE OR REPLACE TABLE sales_data (
  order_id STRING,
  Name STRING,
  Item STRING,
  amount NUMBER
);

-- Load data with CORRECT filename: salesdata.csv
COPY INTO sales_data
FROM @azure_stage/salesdata.csv
FILE_FORMAT = (
  TYPE = 'CSV' 
  FIELD_DELIMITER = ',' 
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
)
ON_ERROR = 'CONTINUE';

-- Check COPY command results
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- Verify data loaded successfully
SELECT 
  CASE 
    WHEN COUNT(*) > 0 THEN '✅ Load Successful'
    ELSE '❌ Load Failed or No Rows Loaded'
  END AS load_status,
  COUNT(*) AS total_rows
FROM sales_data;

-- Preview the loaded data
SELECT * FROM sales_data LIMIT 10;


--create pipe
CREATE OR REPLACE PIPE sales_pipe
AS
COPY INTO SALES_DATA
FROM @azure_stage
FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER=',' SKIP_HEADER=1);

SHOW PIPES;