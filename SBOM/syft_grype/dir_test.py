import os

# Get the current directory
current_directory = os.getcwd()

# List all entries in the directory
entries = os.listdir(current_directory)

print(entries[5])

print(os.listdir(entries[5]))

os.mkdir("directory_test")