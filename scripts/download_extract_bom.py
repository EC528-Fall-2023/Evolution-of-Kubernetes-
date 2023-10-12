'''
download_extract_bom.py
Download list of k8s release files and extract BOM for each release file.

python3 download_extract_bom.py [temp_directory] [BOM storage format] [path to list of versions]
'''
from helper import *
import sys

###Global Variables###
#temp directory, where extraction take place
tdir = "./temp/"
#output directory, where all SBOMs were stored.
odir = "./sboms/"
#enable storage for k8s source.
enable_storage = True
#k8s storage place
stor_dir = "/home/kevin/script_test/storage/"
#Location of BOM tool executable.
bom_exe = "/usr/local/bin/bom"
#Location of wget executable.
wget_exe = "/usr/bin/wget"
#Enable log
enable_log = True
#log location
log_location = "./bom.log"
#base link
#base_link = "https://github.com/kubernetes/kubernetes/releases/tag/"
base_link = "https://github.com/kubernetes/kubernetes/archive/refs/tags/"
#file suffix
file_suffix = ".tar.gz"
#unzip command prefix
unzip_prefix = "/usr/bin/tar"
#result suffix
result_suffix = ".spdx"
#error file
err_path = "./error.log"
#output in spdx, false for json
use_spdx = False
#TO BE IMPLEMENTED switch to extract release vs source
extract_release = True

####Global Variables DO NOT CHANGE####
#path to list of versions
path_to_versions = "./version_list.txt"

#list of errored versions
error_list = []

#process a single version

def getsysarg():
    global tdir, odir, path_to_versions, stor_dir, base_link
    slen = len(sys.argv)
    if slen < 4:
        exit_with_err("Insufficient arguments. Please use python3 download_extract_bom.py [temp_directory] [BOM storage format] [path to list of versions]")
    elif slen == 4:
        tdir = sys.argv[1]
        odir = sys.argv[2]
        path_to_versions = sys.argv[3]
    else:
        exit_with_err("Too many arguments. Please use python3 download_extract_bom.py [temp_directory] [BOM storage format] [path to list of versions].")
    validir(tdir)
    validir(odir)
    validir(stor_dir)
    validir(base_link)
    return tdir, odir, path_to_versions

#process a single file
def process_single(version, enable_storage = enable_storage):
    global error_list
    #obtain full link
    full_url = base_link + version + file_suffix
    #get file name
    filename = version + file_suffix
    #create local directory
    #temp dir
    temp_dir_ver = validir(tdir + version)
    create_dir_if_not_exist(temp_dir_ver)
    #download the file to temp dir
    down_cmd = [wget_exe, "-P", temp_dir_ver, full_url]
    #get the file
    down_code = run_cmd(down_cmd)
    if(down_code != 0):
        #downloading failed, add to error list and stop executing
        add_to_log(log_location, version + " failed to download, skipping...", True, enable_log)
        remove_file_or_dir_linux(temp_dir_ver[:-1])
        return False

    #unzip the tar ball
    unzip_cmd = [unzip_prefix, "-zxvf",  temp_dir_ver + filename, "--directory",temp_dir_ver]
    unzip_code = run_cmd(unzip_cmd)
    if(unzip_code != 0):
        #decompression failed, add to error list and stop execution
        add_to_log(log_location, version + " failed to decompress, skipping...", True, enable_log)
        remove_file_or_dir_linux(temp_dir_ver[:-1])
        return False

    #call the bom tool on extracted directory
    #output path
    output_path = odir + version + result_suffix
    source_path = temp_dir_ver + "kubernetes-" + version[1:]
    bom_cmd = [bom_exe, "generate", source_path, "--output", output_path]
    if(not use_spdx):
        bom_cmd.append("--format")
        bom_cmd.append("json")

    bom_code = run_cmd(bom_cmd)
    #bom_code = print(bom_cmd)
    if(bom_code != 0):
        #bom extraction failed, add to error list and stop execution
        add_to_log(log_location, version + " failed to extract BOM, skipping...", True, enable_log)
        remove_file_or_dir_linux(temp_dir_ver[:-1])
        remove_file_or_dir_linux(output_path)
        return False

    #clean up
    #move downloaded file to storage if enabled
    if(enable_storage):
        move_file_to_linux(temp_dir_ver + filename, stor_dir + filename)
    #remove source otherwise
    else:
        remove_file_or_dir_linux(temp_dir_ver + filename)
    #clear decoompressed directory
    remove_file_or_dir_linux(source_path)

    #process finished, signalthe upper level
    return True


#wrapper
def proc_wrap(versions):
    global error_list
    for i in versions:
        if(not process_single(i,enable_storage)):
            error_list.append(i)
        else:
            add_to_log(log_location, i + " processed successfully.", True, enable_log)
#main function
def main():
    #get command line arguments
    getsysarg()
    add_to_log(log_location, "Hello world! script started.", True, enable_log)
    #read the versions
    versions = get_list_from_file(path_to_versions)

    proc_wrap(versions)

    if(len(error_list) != 0):
        writefile(err_path, error_list)
        add_to_log(log_location, "Found " + str(len(error_list)) + " version(s) failed to process, writing to " + err_path, True, enable_log)

    add_to_log(log_location, "Execution completed, quitting...", True, enable_log)

    return


#invoke the main function
if __name__== "__main__":
    main()
