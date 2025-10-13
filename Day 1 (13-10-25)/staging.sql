CREATE OR REPLACE DATABASE MANAGE_DB;
USE MANAGE_DB;

CREATE SCHEMA IF NOT EXISTS external_stages;

// Publicly accessible staging area    

CREATE OR REPLACE STAGE MANAGE_DB.external_stages.aws_stage
    url='s3://bucketsnowflakes3';

// List files in stage

LIST @MANAGE_DB.external_stages.aws_stage;

//Load data using copy command

CREATE DATABASE IF NOT EXISTS OUR_FIRST_DB;
USE DATABASE OUR_FIRST_DB;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
CREATE OR REPLACE TABLE PUBLIC.ORDERS (
    ORDER_ID       VARCHAR(30),
    CUSTOMER_NAME  VARCHAR(100),
    PRODUCT        VARCHAR(100),
    QUANTITY       NUMBER,
    PRICE          VARCHAR(100)
);


COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
    FROM @MANAGE_DB.external_stages.aws_stage
    file_format= (type = csv field_delimiter=',' skip_header=1 ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE)
    pattern='.*OrderDetails.*';


SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS;



// Create table

CREATE OR REPLACE TABLE ORDERS_CACHING (
ORDER_ID	VARCHAR(30)
,AMOUNT	VARCHAR(30)
,PROFIT	NUMBER(38,0)
,QUANTITY	NUMBER(38,0)
,CATEGORY	VARCHAR(30)
,SUBCATEGORY	VARCHAR(30)
,DATE DATE)   ; 


INSERT INTO ORDERS_CACHING
SELECT
    t1.ORDER_ID,
    t1.PRICE AS AMOUNT,            -- existing column
    0 AS PROFIT,                   -- default value
    t1.QUANTITY,
    t1.PRODUCT AS CATEGORY,        -- map PRODUCT or correct column name
    'N/A' AS SUBCATEGORY,          -- default
    DATE(UNIFORM(1500000000,1700000000,RANDOM())) AS DATE
FROM ORDERS t1
CROSS JOIN (SELECT * FROM ORDERS) t2;