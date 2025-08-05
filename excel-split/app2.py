import pandas as pd

# Read the Excel file
df = pd.read_excel('semester1to3.xlsx')

# Function to split semester columns
def split_semester_column(row, semester):
    value = row.get(semester, "")
    parts = str(value).split('/')
    keys = [
        f"{semester}_ExamSeatNo",
        f"{semester}_Result",
        f"{semester}_Credits",
        f"{semester}_CGPI",
        f"{semester}_CxG",
        f"{semester}_TotalMarks",
        f"{semester}_OutOfMarks",
        f"{semester}_GraceMarks",
        f"{semester}_Exempted"
    ]
    # Fill missing parts with empty strings if any
    parts += [""] * (9 - len(parts))
    return dict(zip(keys, parts))

# List to collect split data
split_data = []

for index, row in df.iterrows():
    new_row = row.to_dict()
    for semester in ['Semester1', 'Semester2', 'Semester3']:
        if semester in row:
            semester_data = split_semester_column(row, semester)
            new_row.update(semester_data)
            # Optionally remove original Semester column
            new_row.pop(semester, None)
    split_data.append(new_row)

# Create new DataFrame
new_df = pd.DataFrame(split_data)

# Export to CSV
new_df.to_csv('output.csv', index=False)

print("✅ CSV file 'output.csv' generated successfully!")
