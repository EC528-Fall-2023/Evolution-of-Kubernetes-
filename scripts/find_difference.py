'''
find_difference.py
Take a list of existing list, compare with all file(s) in a directory, and output those on the list but not present in the directory.
@Kevin Lu
Completed: October 16, 2023
'''
from helper import *

source_directory = "/home/sbom/output/"
source_list = "/home/sbom/list_of_versions_updated"
target_output = "/home/sbom/list_of_versions_1016"

#format RLs
source_directory = validir(source_directory)
##read from the source list
desired_list = get_list_from_file(source_list)
#get list from source dir
actual_list = get_pure_file_name_in_list(get_file_list(source_directory))
#find the differences
new_list = get_new_list_diff(actual_list, desired_list)
#output list to file
writefile(target_output, new_list)
#Make announcement
print("Processed finished, found " + str(len(new_list)) + " missing versions.")