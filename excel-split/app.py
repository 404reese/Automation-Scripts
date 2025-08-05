import pandas as pd

file_name = "test.xlsx"

# Read Excel (no need for header=3 if it's clean)
df = pd.read_excel(file_name)

# Clean column names
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "")
df.columns = df.columns.str.lower()

def split_semester(sem_value):
    if isinstance(sem_value, str):
        parts = sem_value.strip().split('/')
        # We only need first 7 fields
        return parts[:7] + [''] * (7 - len(parts[:7]))
    return [''] * 7

# Extract only needed columns
semester1_data = df[['grno', 'name', 'semester1']].copy()

# Split Semester1
semester1_data[['seat_no', 'result', 'credits_earned', 
                'sgpi', 'cxg', 'mark_earned', 'marks_total']] = semester1_data['semester1'].apply(lambda x: pd.Series(split_semester(x)))

# Drop original Semester1
semester1_data = semester1_data.drop(columns=['semester1'])

# ✅ Final clean table
print(semester1_data)
semester1_data.to_csv("semester1_cleaned.csv", index=False)
