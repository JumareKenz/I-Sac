import os

file_path = "/resources/handouts/DCE102.pdf"
print(f"Checking existence of: {file_path}")

if os.path.exists(file_path):
    print("File exists")
else:
    print("File does not exist")