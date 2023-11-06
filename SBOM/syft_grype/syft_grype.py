# import subprocess
# import os
# import csv
# # import sys

# # Run the grype command with the parsed image name
# def run_grype(k8s_version: str, image_name: str):
    
#     command = [
#         "grype",
#         image_name,
#         "--add-cpes-if-none",
#         "--by-cve",
#         "--json",
#         "--scope", "all-layers",
#         "-o", "grype-table",
#         "-q"
#     ]
#     output_file = 'grype_output.' + image_name + '.json'

#     subprocess.run(command)
#     with open(output_file, 'w') as file:
#         process = subprocess.Popen(
#             command,
#             stdout=file,
#             stderr=subprocess.STDOUT,
#             shell=True
#         )
#         process.communicate()

# #  Run the syft command with the parsed image name
# def run_syft(k8s_version: str, image_name: str):

#     command = [
#         "syft",
#         image_name,
#         "--json",
#         "--scope", "all-layers",
#         "-o", "syft-table",
#         "-q",
#     ]
#     output_file = 'syft_output.' + image_name + '.json'
    
#     subprocess.run(command)
#     with open(output_file, 'w') as file:
#         process = subprocess.Popen(
#             command,
#             stdout=file,
#             stderr=subprocess.STDOUT,
#             shell=True
#         )
#         process.communicate()


# def filter_image_name(name: str):
#     name = name.replace("SPDXRef-Package-k8s.gcr.io-", "k8s.gcr.io/")
#     name = name.replace("SPDXRef-Package-registry.k8s.io-", "registry.k8s.io/")
#     name = name.replace("SPDXREF-Package-k8sgcrio", "k8s.gcr.io/")    
#     name = name.replace("-v",":v")

#     return name

# def process_csv(filename):
#     with open(filename, mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             try:
#                 if "k8s.gcr.io/" in row['PackageName']:
#                     run_syft(row["PackageName"])
#                 elif ".tar" in row['PackageName']:
#                     run_syft(filter_image_name(row['SPDXID']))
#             except Exception as e:
#                 print(e)
#                 continue
    
# if __name__ == "__main__":
#     # if len(sys.argv) != 2:
#     #     print("Usage: python script_name.py your_file.csv")
#     #     sys.exit(1)
    
#     # filename = sys.argv[1]
#     # process_csv(filename)

#     # Get the current directory
#     current_directory = os.getcwd()

#     # List all entries in the directory
#     entries = os.listdir(current_directory)