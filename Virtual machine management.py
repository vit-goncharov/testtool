# -*- coding: utf-8 -*-
"""
Automate define install virtual machine vmware
"""
from __future__ import unicode_literals

import json
import os
import os.path
import string
import subprocess
import sys
import time
from ctypes import windll


def get_drives():
    """
    Get list logical disk on PC
    """
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter + ":\\")
        bitmask >>= 1

    return drives

def define_programm():
    """
    Get list logiacal drive\n
    Find install vm in logical drive\n
    Exist file in curent dir with dict vm:path\n
    Return dict vm:path
    """
    list_programm = {}
    device = get_drives()
    print "Found Logical Drive " + str(device)
    for dev in device:
        if os.path.exists(dev):
            for root, dirs, files in os.walk(dev):
                for file_name in files:
                    if file_name[-4:] == '.vmx':
                        path_apps = os.path.join(root, file_name)
                        list_programm[file_name] = path_apps
                        print "Found " + file_name + " in " + path_apps
                    if file_name == 'vmrun.exe':
                        path_apps = os.path.join(root, file_name)
                        list_programm[file_name] = path_apps

    with open('vm_list.txt', 'w') as outfile:
        json.dump(list_programm, outfile)
    return list_programm

def get_vmrun():
    """
    Get path to vmrun
    """
    with open('vm_list.txt', 'r') as infile:
        list_apps = json.load(infile)
        return list_apps["vmrun.exe"]

def vm_mode(app, mode, hardsoft):
    """
    Call mode vmware start/stop/reset
    """
    vmrun_path = get_vmrun()
    print mode + " vm"
    subprocess.call([vmrun_path,
                     "-T",
                     "ws",
                     mode,
                     app,
                     hardsoft],
                    shell=True)

def sleep_vm(vm_file, user="user", password="qwerty"):
    """
    sleep virtual machine func
    """
    vmrun_path = get_vmrun()
    print "sleep vm"
    subprocess.call([vmrun_path,
                     "-T",
                     "ws",
                     "-gu",
                     str(user),
                     "-gp",
                     str(password),
                     "runProgramInGuest",
                     vm_file,
                     "cmd.exe",
                     "/c rundll32.exe Powrprof.dll,SetSuspendState 0,,1"],
                    shell=True)

def get_list_app():
    """
    return list app
    """
    if os.path.exists('vm_list.txt'):
        req = raw_input("Do you want refrash vm list? (y/n) -> ").lower()
        if req == "y":
            list_apps = define_programm()
            return list_apps
        else:
            with open('vm_list.txt', 'r') as infile:
                list_apps = json.load(infile)
                return list_apps
    else:
        list_apps = define_programm()
        return list_apps

def get_app(list_apps):
    """
    view list vm install on PC\n
    found app on number\n
    return choise app
    """
    print "\nLists vm in PC:"
    numb_app = {}
    indx = 1
    for keys in sorted(list_apps):
        if keys != "vmrun.exe":
            numb_app[str(indx)] = keys
            print "[" + str(indx) + "]" + " - " + keys
            indx = indx + 1

    while True:
        numb = raw_input("Select an app in list above -> ")
        if numb in numb_app:
            if numb_app[numb] in list_apps:
                app = numb_app[numb]
                print "Done"
                break
            else:
                print "Invalid name apps, try again"
        else:
            print "Intalid value, please try again"
    return app.encode('utf-8')

def main():
    """
    General functions
    """
    reload(sys)
    encoding = sys.getfilesystemencoding()
    sys.setdefaultencoding(encoding)

    commands = ["start", "stop", "suspend", "reset"]
    mods_command = ["hard", "soft", "gui", "nogui"]

    list_apps = get_list_app()

    if "vmrun.exe" not in list_apps:
        print "Vmware Workstation not installed on this PC"
        return 0
    elif len(list_apps) == 1:
        print "vm not found"
        return 0

    app = get_app(list_apps)

    print "Command: \n\
           start [gui/nogui] \n\
           stop [hard/soft] \n\
           reset [hard/soft] \n\
           sleep [soft] \n\
           suspend [hard/soft] \n\
           test [soft] \n\
           q - quite \n"

    while True:
        comand = raw_input("Take command (ex. start) -> ").lower()
        if comand == "q":
            break

        while True:
            mods = raw_input("Take mods command [] -> ").lower()
            if mods in mods_command:
                break
            else:
                print "Invalid mode parametr, try again"

        if comand == "test":
            vm_mode(list_apps[app], "reset", "soft")
            time.sleep(30)
            vm_mode(list_apps[app], "stop", "hard")
            time.sleep(15)
            vm_mode(list_apps[app], "start", "gui")
            time.sleep(40)
            sleep_vm(list_apps[app])
            time.sleep(15)
            vm_mode(list_apps[app], "start", "gui")
        elif comand in commands:
            vm_mode(list_apps[app], comand, mods)
        elif comand == "sleep":
            user = raw_input("vm user -> ")
            password = raw_input("user password -> ")
            sleep_vm(list_apps[app], user, password)
        else:
            print "Invalid command, please try again"

if __name__ == "__main__":
    main()
