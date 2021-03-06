import paramiko
import pprint
import sys
import argparse as arg
import subprocess
import logging as logger

centOS={'ip':'172.16.201.2','port':'22'}
ubuntu={'ip':'172.16.201.1','port':'22'}
OSs={'centOS':centOS,'ubuntu':ubuntu}

private_key_path='/root/.ssh/id_rsa'

def ssh_connect(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='root',port=22, key_filename=private_key_path)
    return ssh

def set_ip_centOS(ssh_c,ip):
    ssh_c.exec_command(r"sed 's/\(IPADDR=\).*/\1%s/g' -i /etc/sysconfig/network-scripts/ifcfg-ens160" %(ip))
    print('changing ip address '.ljust(30,'.')+' done')
    try:
        ssh_c.exec_command('systemctl restart network',timeout=1000)
    except :
        print('previous connection closed')

def set_ip_ubuntu(ssh_c,ip):
    ssh_c.exec_command(r"sed 's/\(.*address\) \(.*\)/\1 %s/g' -i /etc/network/interfaces" %(ip))
    print('changing ip address '.ljust(30,'.')+' done')
    try:
        ssh_c.exec_command('systemctl restart networking && ip addr del 172.16.201.1/16 dev ens160 && systemctl restart networking',timeout=1000)
    except :
        print('previous connection closed')

def setup(ssh_c,ip,hostname,os):
    ssh_c.exec_command(f'hostnamectl set-hostname {hostname}')
    print('changing the hostname '.ljust(30,'.')+' done')

    if os =='centOS':
        set_ip_centOS(ssh_c,ip)
    else:
        set_ip_ubuntu(ssh_c,ip)

    print('restarting the network '.ljust(30,'.')+' done')

def add_to_bastilion(host,username,password):
    cmd = subprocess.Popen(["./bastilion-add-server.sh",username,password,host['name'],host['ip'],f"{host['port']}"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    cmd.communicate()
    if cmd.returncode == 0:
        print(f"server {host['name']} with ip {host['ip']} added to bastilion server")
    else:
        logger.warning(f"something went wrong during adding server {host['name']} with ip {host['ip']} to bastilion server")

def pars_flags():
    arg_parser= arg.ArgumentParser()
    arg_parser.add_argument('--bastilion_username',action='store',type=str,required=True)
    arg_parser.add_argument('--bastilion_password',action='store',type=str,required=True)
    arg_parser.add_argument('--os',action='store',type=str,required=True)
    arg_parser.add_argument('--hostname',action='store',type=str,required=True)
    arg_parser.add_argument('--ip',action='store',type=str,required=True)
    arg_parser.add_argument('--port',action='store',type=str,required=False,default=22)
    return arg_parser.parse_args()


flags=pars_flags()
ssh_c=ssh_connect(OSs[flags.os]['ip'])
setup(ssh_c,flags.ip,flags.hostname,flags.os)
ssh_c.close()

host={'ip':flags.ip,'port':flags.port,'name':flags.hostname}
add_to_bastilion(host,flags.bastilion_username,flags.bastilion_password)