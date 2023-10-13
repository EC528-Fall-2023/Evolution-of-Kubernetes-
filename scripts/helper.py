import progressbar, shutil, os, subprocess, glob, multiprocessing, ntpath, shlex, filecmp
import requests as req
from datetime import datetime
from multiprocessing.pool import ThreadPool

#get current date and time as yyyy_mm_dd_hh_mm_ss
def get_datetime(style = 0):
    now = datetime.now()
    if(style == 0):
        dt_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    elif(style == 1):
        dt_string = now.strftime("%Y_%m_%d_%H%M%S")
    elif(style == 2):
        dt_string = now.strftime("%Y%m%d_%H%M%S")
    elif(style == 3):
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    elif(style == 4):
        dt_string = now.strftime("%m/%d %H:%M:%S")
    elif(style == 5):
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

# add to the log file
def add_to_log(fdir, content, print_c=True, enable_log=True, prefix_cus=""):
    prefix = "[" + get_datetime(4) + "] " + prefix_cus + " "
    line = prefix + content
    if (print_c):
        print(line)
    else:
        pass

    if (enable_log):
        file = open(fdir, 'a')
        # write new line first
        file.write("\n")
        file.write(line)
        file.close()
    else:
        pass
    return

#Exit python with provided error message
def exit_with_err(emsg):
    print(emsg)
    exit(1)

#return content of a single file as list
def get_list_from_file(fdir):
    file1 = open(fdir, 'r')
    Lines = file1.read().splitlines()
    return Lines

#validate url is in correct format
#by default replace all "\" with "/", add "/" at the end if not exist.
#if replace == False, no replace happens. if inputurl ends with "/" or "\" nothing happens, else "/" will be appended.
def validir(inputurl, replace = True):
    if (replace == True):
        inputurl = inputurl.replace("\\", "/")
        if (inputurl[-1] == "/"):
            return inputurl
        return (inputurl + "/")
    else:
        if (inputurl[-1] == "/" or "\\"):
            return inputurl
        return (inputurl + "/")
#Create if dir not exist
def create_dir_if_not_exist(inputdir, msg = "Folder Created: ", Print = True, appenddir = True):
    inputdir = validir(inputdir)
    exist = os.path.exists(inputdir)
    if (not exist):
        os.makedirs(inputdir)
        if(Print):
            if(appenddir):
                print(msg + str(inputdir))
            else:
                print(msg)
        else:
            pass
    else:
        pass
    return

#run a system command, accepting list of arguments
def run_cmd(fcmd, shell = False):
    #os.system(fcmd)
    #print("cmd called")
    if(shell):
        print(serialize_cmd(fcmd))
        c = subprocess.call(serialize_cmd(fcmd), shell=True)
        return c
    else:
        c = subprocess.call(fcmd)
        return c
    return None

#serialize command
def serialize_cmd(cmd):
    if(cmd == []):
        return ''
    else:
        res = ''
        for i in cmd:
            res += i
            res += ' '
        #remove last space
        res = res[:-1]
        return res
    return ''

#Move a file to another directory & overwrite linux
def move_file_to_linux(ori, dest):
    cmd = ["mv", "-f", ori, dest]
    run_cmd(cmd)
    return


#remove a file or a dir
def remove_file_or_dir_linux(wdir):
    cmd = ["rm", "-rf", wdir]
    run_cmd(cmd)
    return

#write a specific file to a system location with content
def writefile(filename, content, print_progress = True):
    res = open(filename, "w")
    if(print_progress):
        lenf1 = len(content)
        bar = progressbar.ProgressBar(maxval=lenf1, \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        cnt = 0
        for i in content:
            res.write(str(i))
            res.write("\n")
            cnt += 1
            bar.update(cnt)
        bar.finish()
    else:
        for i in content:
            res.write(str(i))
            res.write("\n")
    res.close()
