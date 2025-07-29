import sys
import os
import re
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Inputs from GitHub Action
issue_title = sys.argv[1]
issue_body = sys.argv[2]

# Parse TLG ID and Title from issue title
match = re.match(r"\[TLG\]\s*-\s*(.*?)\s*-\s*(.*)", issue_title)
if not match:
    print("Issue title format not recognized. Use: [TLG] - TLG_ID - Title")
    sys.exit(1)

tlg_id = match.group(1).strip()
title = match.group(2).strip()

# Attempt to extract programmer and QC reviewer from body
def extract_field(label):
    m = re.search(rf"\*\*{label}\*\*:\s*@?(\w+)", issue_body)
    return m.group(1) if m else ""

programmer = extract_field("Programmer")
qc_reviewer = extract_field("QC Reviewer")

# Determine subfolder from TLG ID prefix
folder_map = {
    'T': 'tables',
    'L': 'listings',
    'F': 'figures'
}
type_prefix = tlg_id[0].upper()
subfolder = folder_map.get(type_prefix, 'misc')

# Construct filename
filename = f"programs/{subfolder}/{tlg_id.replace('.', '_')}_{title.replace(' ', '_')}.ipynb"
os.makedirs(os.path.dirname(filename), exist_ok=True)

# Create notebook content
nb = new_notebook(cells=[
    new_markdown_cell(f"""
# 📊 TLG Analysis Notebook

- **TLG ID**: {tlg_id}  
- **Title**: {title}  
- **Programmer**: @{programmer}  
- **QC Reviewer**: @{qc_reviewer}  
"""),
    new_code_cell("""
# Load ADaM datasets
# df_adsl = spark.read.format("delta").table("adam.adsl")
""")
])

# Write notebook file
with open(filename, 'w') as f:
    nbformat.write(nb, f)

print(f"Notebook created: {filename}")
