"""
tests module, differents code to tessting new functions
"""
import os
import os.path
import subprocess
import sys
import time

SYSTEMROOT = str(os.path.expandvars("%SYSTEMROOT%")) #Example C:\Windows
PROGRAM_FILESX86 = str(os.path.expandvars("%PROGRAMFILES(x86)%"))
PROGRAM_FILES = str(os.path.expandvars("%PROGRAMFILES%"))

LIST_APP = {
    "AcroRd32.exe":"Adobe Reader",
    "WINWORD.EXE":"MS Word",
    "EXCEL.EXE":"MS Excel",
    "chrome.exe":"Chrome",
    "iexplore.exe":"Internet explorer",
    "firefox.exe":"Firefox",
    "opera.exe":"Opera",
    "Skype.exe":"Skype",
    "WinRAR.exe":"WinRaR",
    "notepad++.exe":"Notepad++"
}

def helps(mode):
    """
    Help manual and example
    """
    if mode == "varible":
        print "Please take valid argument\n\
              Argument is time delay in int second\n\
              This delay between start and close prog\n\
              Argument is count this is count call script\n\
              Argument must be > 0"

    if mode == "flag":
        print "Invalid or miss flag!\n\
               flag mode:\n\
               -a auto mode\n\
               -s settings mode\n\
               example: name_script.py -s"

def loop_list_prog(lists, mode):
    """
    loop in list programm with start programm or close
    """
    if str(mode) == "s":
        for key in lists:
            subprocess.Popen(str(lists[key][1]), shell=True)
            print "Starting " + key
            time.sleep(3)
    elif str(mode) == "c":
        for key in lists:
            print "Closing " + key
            subprocess.call(["taskkill", "/f", "/im", str(lists[key][0])], shell=True)
            time.sleep(3)
    else:
        print "Invalid mode argument"
        sys.exit(1)

def start_testing(lists_programm, delay):
    """
    Start testtig func
    """
    loop_list_prog(lists_programm, "s")
    print "I wait " + str(delay) + " sec, after I close programm"
    time.sleep(delay)
    loop_list_prog(lists_programm, "c")

def define_programm(path_to_prg, list_apps):
    """
    Find install programm in system drive
    """
    print path_to_prg
    if os.path.exists(path_to_prg):
        list_programm = {}
        for root, dirs, files in os.walk(path_to_prg):
            for file_name in files:
                for key in list_apps:
                    if file_name == key:
                        path_apps = os.path.join(root, file_name)
                        list_programm[list_apps[key]] = [key, path_apps]
                        print "Found " + list_apps[key] + " in " + path_apps

    return list_programm

def main():
    """
    general func
    """
    if len(sys.argv) < 2:
        helps("flag")
        return 0

    if sys.argv[1] == "-a":
        if os.path.exists(PROGRAM_FILESX86):
            list_prog = define_programm(PROGRAM_FILESX86, LIST_APP)
            start_testing(list_prog, 20)
            return 0
        else:
            list_prog = define_programm(PROGRAM_FILES, LIST_APP)
            start_testing(list_prog, 20)
            return 0

    elif sys.argv[1] == "-s":
        delay = int(raw_input("Take delay bettwen start and close prog -> "))
        count = int(raw_input("Take count loop pass -> "))

        if os.path.exists(PROGRAM_FILESX86):
            list_prog = define_programm(PROGRAM_FILESX86, LIST_APP)
        else:
            list_prog = define_programm(PROGRAM_FILES, LIST_APP)

        if delay == 0 or count == 0:
            helps("varible")
            return 0

        while count:
            print "Still loop pass " + str(count)
            start_testing(list_prog, delay)
            count = count - 1
    else:
        helps("flag")
        return 0


if __name__ == "__main__":
    main()
