import pandas as pd

# Read source data
df = pd.read_csv('employee_sales_source.csv')

print("=== BEFORE CLEANING ===")
print(f"Total Records: {len(df)}")
print(f"Null values:\n{df.isnull().sum()}\n")

# --------------------------------------------
# RULE 1: Remove Duplicate Records
# --------------------------------------------
print("RULE 1: Removing duplicates...")
initial_count = len(df)
df = df.drop_duplicates()
removed_duplicates = initial_count - len(df)
print(f"Removed {removed_duplicates} duplicate records")

# --------------------------------------------
# RULE 2: Remove Records with Null Employee Names
# --------------------------------------------
print("\nRULE 2: Removing records with missing employee names...")
initial_count = len(df)
df = df[df['employee_name'].notna()]
removed_null_names = initial_count - len(df)
print(f"Removed {removed_null_names} records with null names")

# --------------------------------------------
# RULE 3: Standardize Employee Names (Title Case)
# --------------------------------------------
print("\nRULE 3: Standardizing employee names to Title Case...")
df['employee_name'] = df['employee_name'].str.title()
print("Names standardized")

# --------------------------------------------
# RULE 4: Standardize Department Names (Title Case)
# --------------------------------------------
print("\nRULE 4: Standardizing department names...")
df['department'] = df['department'].str.title()
print("Department names standardized")

# --------------------------------------------
# RULE 5: Fill Missing Departments with 'Unknown'
# --------------------------------------------
print("\nRULE 5: Filling missing departments...")
df['department'] = df['department'].fillna('Unknown')
print("Missing departments filled with 'Unknown'")

# --------------------------------------------
# RULE 6: Remove Records with Invalid Salary (negative or null)
# --------------------------------------------
print("\nRULE 6: Removing invalid salary records...")
initial_count = len(df)
df = df[(df['salary'] > 0) & (df['salary'].notna())]
removed_invalid_salary = initial_count - len(df)
print(f"Removed {removed_invalid_salary} records with invalid salary")

# --------------------------------------------
# RULE 7: Standardize Date Format
# --------------------------------------------
print("\nRULE 7: Standardizing date format...")
df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
df['join_date'] = df['join_date'].dt.strftime('%Y-%m-%d')
print("Date format standardized to YYYY-MM-DD")

# --------------------------------------------
# RULE 8: Remove Records with Invalid Dates
# --------------------------------------------
print("\nRULE 8: Removing records with invalid dates...")
initial_count = len(df)
df = df[df['join_date'].notna()]
removed_invalid_dates = initial_count - len(df)
print(f"Removed {removed_invalid_dates} records with invalid dates")

# --------------------------------------------
# RULE 9: Standardize Email to Lowercase
# --------------------------------------------
print("\nRULE 9: Standardizing emails to lowercase...")
df['email'] = df['email'].str.lower()
print("Emails standardized to lowercase")

# --------------------------------------------
# RULE 10: Fill Missing Emails with Default Pattern
# --------------------------------------------
print("\nRULE 10: Filling missing emails...")
df['email'] = df['email'].fillna('noemail@company.com')
print("Missing emails filled with default")

# Save cleaned data (this is your target data)
df.to_csv('employee_sales_target.csv', index=False)

print("\n=== AFTER CLEANING ===")
print(f"Total Records: {len(df)}")
print(f"Null values:\n{df.isnull().sum()}\n")
print(df)
print("\n✅ Cleaned data saved to 'employee_sales_target.csv'")