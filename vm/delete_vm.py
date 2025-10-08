#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Ключ true - Удаляет диски vm
# Пример запуска: ./delete_vm.py d0test0-xxc001-3lk_delete.csv true


import os
import time
import sys
import array
import datetime
import hashlib


IMG_DIR="/opt/libvirt/IMG"
VM_DIR="/opt/libvirt/images"







def DelVmConf(VmName):

    StatusCmd="virsh domstate "+VmName+" | awk '{print $(NF)}' | tr -d '\n'"
    StatusVm = os.popen(StatusCmd).read()
    os.popen(StatusCmd).close()
    print(StatusVm)
    if str(StatusVm) == "off":
        print('выключенно')
        os.system('virsh start '+VmName)
        time.sleep(10)
    os.system('virsh undefine '+VmName)
    time.sleep(5)
    os.system('virsh destroy '+VmName)
    time.sleep(10)
   






















file1 = open(sys.argv[1], "r")

while True:
   
    line = file1.readline()
    
    if not line:
        break
    
    VM_NAME=line.strip().split(",")[0]
    
    print(line.strip())
    if int(len(sys.argv))==3:
        if sys.argv[2] == "true":
            print("Удаление дисков")
            CmdRun="virsh domstats "+VM_NAME+" | grep -w "+VM_DIR+" | tr '=' ' ' | awk '{print $NF}' | tr '\n' ', '| tr -d '\n'"
            PachHdd = os.popen(CmdRun).read()
            os.popen(CmdRun).close()
            PachHdd=PachHdd.split(",")
            print(PachHdd)
            StatusCmd="virsh domstate "+VM_NAME+" | awk '{print $(NF)}' | tr -d '\n'"
            StatusVm = os.popen(StatusCmd).read()
            os.popen(StatusCmd).close()
            print(StatusVm)
            if str(StatusVm) == "off":
                print('выключенно')
                os.system('virsh start '+VM_NAME)
                time.sleep(10)
            os.system('virsh undefine '+VM_NAME)
            time.sleep(5)
            os.system('virsh destroy '+VM_NAME)
            time.sleep(10)
            for f in PachHdd:
                if int(len(f)) != 0:
                    #print('rm -rf '+str(f))
                    os.system('rm -rf '+str(f))
                              
            time.sleep(5)
        else:
             DelVmConf(VM_NAME)

    else:
        DelVmConf(VM_NAME)
   
file1.close



