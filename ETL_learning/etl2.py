import pandas as pd
import re

# ==============================================
# 🧹 ETL DATA CLEANING SCRIPT (Employee Dataset)
# ==============================================

# Read source data
df = pd.read_csv('employee_sales_source.csv')
print(f"Initial Records: {len(df)}")

# --------------------------------------------
# RULE 1: Remove Duplicates
# --------------------------------------------
df = df.drop_duplicates()

# --------------------------------------------
# RULE 2: Remove Null or Blank Employee Names
# --------------------------------------------
df = df[df['employee_name'].notna() & (df['employee_name'].str.strip() != '')]

# --------------------------------------------
# RULE 3: Trim Spaces & Standardize Name and Department (Title Case)
# --------------------------------------------
df['employee_name'] = df['employee_name'].str.strip().str.title()
df['department'] = df['department'].fillna('Unknown').str.strip().str.title()

# --------------------------------------------
# RULE 4: Validate and Clean Salary
# - Remove null or negative salary
# - Remove extreme outliers (optional threshold)
# --------------------------------------------
df = df[df['salary'].notna() & (df['salary'] > 0)]
salary_threshold = df['salary'].quantile(0.99)  # Remove top 1% outliers
df = df[df['salary'] <= salary_threshold]

# --------------------------------------------
# RULE 5: Standardize & Validate Dates
# --------------------------------------------
df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
df = df[df['join_date'].notna()]
df['join_date'] = df['join_date'].dt.strftime('%Y-%m-%d')

# --------------------------------------------
# RULE 6: Standardize & Validate Emails
# --------------------------------------------
df['email'] = df['email'].fillna('noemail@company.com').str.lower().str.strip()

# Basic email format validation
valid_email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
df['email_valid'] = df['email'].apply(lambda x: bool(re.match(valid_email_pattern, x)))
invalid_emails = df[~df['email_valid']]
if not invalid_emails.empty:
    print(f"Removed {len(invalid_emails)} invalid emails")
df = df[df['email_valid']]
df = df.drop(columns=['email_valid'])

# --------------------------------------------
# RULE 7: Calculate Derived Fields (Optional)
# e.g., Annual Bonus = 10% of Salary
# --------------------------------------------
df['annual_bonus'] = df['salary'] * 0.10

# --------------------------------------------
# RULE 8: Final Sanity Checks
# --------------------------------------------
df = df.dropna(subset=['employee_name', 'department', 'salary', 'join_date'])

# Save the cleaned data
df.to_csv('employee_sales_target.csv', index=False)

# --------------------------------------------
# Summary
# --------------------------------------------
print("\n✅ CLEANING COMPLETE")
print(f"Final Records: {len(df)}")
print(f"Null values after cleaning:\n{df.isnull().sum()}\n")
print(df.head())
print("\nCleaned file saved as: employee_sales_target.csv")
