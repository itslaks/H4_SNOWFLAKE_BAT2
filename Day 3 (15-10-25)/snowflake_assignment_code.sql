-- 1. Create Database and Schema
CREATE OR REPLACE DATABASE company_db;
CREATE OR REPLACE SCHEMA analytics;

-- 2. Create Table
CREATE OR REPLACE TABLE analytics.employees (
    emp_id INT,
    first_name STRING,
    last_name STRING,
    department STRING,
    salary FLOAT
);

-- 3. Insert Sample Data
INSERT INTO analytics.employees VALUES
(1, 'Alice', 'Johnson', 'HR', 60000),
(2, 'Bob', 'Smith', 'IT', 80000),
(3, 'Charlie', 'Brown', 'Finance', 75000);


SELECT * FROM analytics.employees;

SELECT * FROM analytics.employees_transformed;


USE DATABASE COMPANY_DB;
USE SCHEMA ANALYTICS;

SHOW TABLES;


