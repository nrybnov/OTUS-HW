#!/usr/bin/python3
# -*- coding: UTF-8 -*-


# Содержание csv файла
#Имя манины,кол-во ядер CPU,RAM,образ OS,диски, через пробел(название=емкость=тип=формат),тип OS,сеть( через пробел: ""-DHCP , "none"-без сетевого интерфейса,"111.111.111.111"-статический адрес)
#test-test001lk,2,2048,astra-174-tmpl,"system=30=sata=qcow2 hdd001_pg_data=10=sata=qcow2",linux2022,""






import os
import time
import sys
import array
import datetime
import hashlib
from pathlib import Path
import paramiko

IMG_DIR="/opt/libvirt/IMG"
VM_DIR="/opt/libvirt/images"
#VM_DIR="/opt/libvirt/service-images/images"
USER="root"
PASSWORD="1234567"
DEFOULT_IP="10.10.0.254"













def SetupNetworkInterface(st,val,vm_n):
    if int(st)==1:
        print('Настройка адреса DHCP...')
        os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
        stdin, stdout, stderr = client.exec_command("ip a | grep -w '2:'")
        data = stdout.read() + stderr.read()
        print(str(data).split(" ")[1].replace(':', '').rstrip())
        client.exec_command('sed -i \'/address\ ' +DEFOULT_IP+ '/,+10d\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/iface\ '+str(data).split(" ")[1].replace(':', '').rstrip()+'\ inet\ static/iface\ '+str(data).split(" ")[1].replace(':', '').rstrip()+'\ inet\ dhcp/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
        client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
        client.exec_command('reboot')
        client.close()
        time.sleep(10)
    elif int(st)==2:
        os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
        stdin, stdout, stderr = client.exec_command("ip a | grep -w '2:'")
        data = stdout.read() + stderr.read()
        print(str(data).split(" ")[1].replace(':', '').rstrip())
        client.exec_command('sed -i \'s/auto eth0/auto '+str(data).split(" ")[1].replace(':', '').rstrip()+'/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/allow-hotplug eth0/allow-hotplug '+str(data).split(" ")[1].replace(':', '').rstrip()+'/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/iface eth0 inet static/iface '+str(data).split(" ")[1].replace(':', '').rstrip()+' inet static/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/address '+DEFOULT_IP+'/address '+val+'/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/network 10.10.0.0/network '+val.split(".")[0]+'.'+val.split(".")[1]+'.'+val.split(".")[2]+'.0/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/broadcast 10.10.0.255/broadcast '+val.split(".")[0]+'.'+val.split(".")[1]+'.'+val.split(".")[2]+'.255/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/gateway 10.10.0.1/gateway '+val.split(".")[0]+'.'+val.split(".")[1]+'.'+val.split(".")[2]+'.1/\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
        client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
        client.exec_command('reboot')
        client.close()
        time.sleep(10)
    elif int(st)==3:
        CmdRun="virsh domiflist "+vm_n+" | grep -w virtio | awk '{print $2\"|\"$5}' | tr -d '\n'"
        data = os.popen(CmdRun).read()
        os.popen(CmdRun).close()
        if_data=data.split('|')
        os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
        client.exec_command('sed -i \'/auto eth0/,+10d\' /etc/network/interfaces')
        client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
        client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
        client.exec_command('reboot')
        client.close()
        os.system('virsh detach-interface --domain '+vm_n+' --type '+str(if_data[0])+' --mac '+str(if_data[1]))
        time.sleep(15)
        os.system('virsh dumpxml '+vm_n+' > /tmp/'+vm_n+'.xml')
        time.sleep(5)
        os.system('virsh define /tmp/'+vm_n+'.xml')
        time.sleep(5)
        os.remove('/tmp/'+vm_n+'.xml')
        time.sleep(10)
    elif int(st)==4:
        print('Настройка адреса DHCP Ubuntu...')
        os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
        stdin, stdout, stderr = client.exec_command("ip a | grep -w '2:'")
        data = stdout.read() + stderr.read()
        print(str(data).split(" ")[1].replace(':', '').rstrip())
        client.exec_command('cat /dev/null > /etc/netplan/00-installer-config.yaml')
        client.exec_command("echo -e '# This is the network config written by \'subiquity\'' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e  'network:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '  ethernets:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '    "+str(data).split(" ")[1].replace(':', '').rstrip()+":' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '      dhcp4: true' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '  version: 2' >> /etc/netplan/00-installer-config.yaml;")
        client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
        client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
        client.exec_command('netplan generate')
        client.exec_command('reboot')
        client.close()
        time.sleep(10)
    elif int(st)==5:
        print('Настройка адреса в ручную Ubuntu...')
        os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
        time.sleep(15)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
        stdin, stdout, stderr = client.exec_command("ip a | grep -w '2:'")
        data = stdout.read() + stderr.read()
        print(str(data).split(" ")[1].replace(':', '').rstrip())
        If=str(data).split(" ")[1].replace(':', '').rstrip()
        client.exec_command('cat /dev/null > /etc/netplan/00-installer-config.yaml')
        time.sleep(3)
        client.exec_command("echo -e \'# This is the network config written by \'subiquity\'' >> /etc/netplan/00-installer-config.yaml; \n\
echo -e 'network:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '  ethernets:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '    "+str(If)+":' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '       dhcp4: no' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '       addresses:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '         - "+str(val)+"/24' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '       nameservers:' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '         addresses: [192.168.15.1, 192.168.15.9]' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '       gateway4: "+val.split(".")[0]+'.'+val.split(".")[1]+'.'+val.split(".")[2]+".1' >> /etc/netplan/00-installer-config.yaml;\n\
echo -e '  version: 2' >> /etc/netplan/00-installer-config.yaml;")

        client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
        client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
        client.exec_command('netplan generate')
        client.exec_command('reboot')
        client.close()
        del client
        time.sleep(10)
    else:
        if int(st)==6:
            print('Нет сетевого интерфейса Ubuntu...')
            CmdRun="virsh domiflist "+vm_n+" | grep -w virtio | awk '{print $2\"|\"$5}' | tr -d '\n'"
            data = os.popen(CmdRun).read()
            os.popen(CmdRun).close()
            if_data=data.split('|')
            os.system('ssh-keygen -f "${HOME}/.ssh/known_hosts" -R "10.10.0.254"')
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=DEFOULT_IP, username=USER, password=PASSWORD, port="22")
            client.exec_command('cat /dev/null > /etc/netplan/00-installer-config.yaml')
            client.exec_command("echo -e '# This is the network config written by \'subiquity\'' >> /etc/netplan/00-installer-config.yaml")
            client.exec_command('sed -i \'s/orig-img/'+vm_n+'/\' /etc/hosts')
            client.exec_command('echo -e "'+vm_n+'" > /etc/hostname')
            client.exec_command('reboot')
            client.close()
            os.system('virsh detach-interface --domain '+vm_n+' --type '+str(if_data[0])+' --mac '+str(if_data[1]))
            time.sleep(15)
            os.system('virsh dumpxml '+vm_n+' > /tmp/'+vm_n+'.xml')
            time.sleep(5)
            os.system('virsh define /tmp/'+vm_n+'.xml')
            time.sleep(5)
            os.remove('/tmp/'+vm_n+'.xml')
            time.sleep(10)    



















def main():
    file1 = open(sys.argv[1], "r")


    while True:
        print('Запуск')

        line = file1.readline()
        
        if not line:
            break
        
        if str(line.strip()[0]) == '#':
            continue


        VM_NAME=line.strip().split(",")[0]
        CPU=line.strip().split(",")[1]
        RAM=line.strip().split(",")[2]
        IMAGE_OS=line.strip().split(",")[3]   
        print('Запрос: '+str(line.strip()))
        HDDS=line.strip().split(",")[4].replace('"', '').split(" ")
        #print(len(HDDS))
        hdd_params=""
        for i in range(len(HDDS)):       # Пока 1 - только системный диск
            #print(HDDS[i].split("="))
            SYSDISK=VM_NAME+"_"+HDDS[0].split("=")[0]
            DISK_SIZE=HDDS[i].split("=")[1]
            DISK_TYPE=HDDS[i].split("=")[2]
            VM_DISK_FORMAT=HDDS[i].split("=")[3]
            #print(i)
            hdd_params=hdd_params+" --disk path="+VM_DIR+"/"+VM_NAME+"_"+HDDS[i].split("=")[0]+".qcow2,size="+DISK_SIZE+",bus="+DISK_TYPE+",format="+VM_DISK_FORMAT+" "
        OS_VARIANT=line.strip().split(",")[5]
    
        #print(hdd_params)
        NETWORKS=line.strip().split(",")[6]
        NETWORKS=NETWORKS.replace('"', '')
        
         
        


       
        print('Копирование образа '+IMAGE_OS+'...')    
        os.system('rsync -arv --progress '+IMG_DIR+'/'+IMAGE_OS+'.'+VM_DISK_FORMAT+' '+VM_DIR+'/'+SYSDISK+'.'+VM_DISK_FORMAT)
        print('Скопирован')
        time.sleep(10)
       
        print('Создание ВМ...')
        os.system('virt-install -n '+VM_NAME+' -r '+RAM+' --vcpus='+CPU+' --cpu host --check-cpu --os-variant='+OS_VARIANT+' --import  '+hdd_params+'  --graphics vnc,listen=0.0.0.0  -w bridge:br0 --boot hd,menu=on --noautoconsole')
        time.sleep(30)

        print('len сети '+str(len(NETWORKS)))

        if str(IMAGE_OS) == "ubuntu-20.04-tmpl":
            if int(len(NETWORKS)) == 0:
                print('DHCP ubuntu-20.04')
                SetupNetworkInterface('4','1',str(VM_NAME))
            else:
                if str(NETWORKS) == "none":
                    print('Без сетевого интерфейса. ubuntu-20.04')
                    SetupNetworkInterface('6','1',str(VM_NAME))
                else:
                    print('Статика в ручную ubuntu-20.04')
                    SetupNetworkInterface('5',str(NETWORKS),str(VM_NAME))

        else:
            if int(len(NETWORKS)) == 0:
                print('DHCP')
                SetupNetworkInterface('1','1',str(VM_NAME))
            else:
                if str(NETWORKS) == "none":
                    print('Без сетевого интерфейса.')
                    SetupNetworkInterface('3','1',str(VM_NAME))
                else:
                    print('Статика в ручную')
                    SetupNetworkInterface('2',str(NETWORKS),str(VM_NAME))
            
    
        
    file1.close
    print("Успех.")





main()
