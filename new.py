import argparse as arg
import subprocess
import logging as logger

def add_to_bastilion(host,username,password):
    cmd = subprocess.Popen(["./bastilion-add-server.sh",username,password,host['name'],host['ip'],f"{host['port']}"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    cmd.communicate()
    if cmd.returncode == 0:
        print(f"server {host['name']} with ip {host['ip']} added to bastilion server")
    else:
        logger.warning(f"something went wrong during adding server {host['name']} with ip {host['ip']} to bastilion server")

def pars_flags():
    arg_parser= arg.ArgumentParser()
    arg_parser.add_argument('--bastilion-username',action='store',type=str,required=True)
    arg_parser.add_argument('--bastilion-password',action='store',type=str,required=True)
    
    arg_parser.add_argument('--os',action='store',type=str,required=True)
    arg_parser.add_argument('--hostname',action='store',type=str,required=True)
    arg_parser.add_argument('--ip',action='store',type=str,required=True)
    arg_parser.add_argument('--port',action='store',type=int,required=False,default=22)

    return arg_parser.parse_args()


flags=pars_flags()
host={'name':flags.hostname,'ip':flags.ip,'port':flags.port}
add_to_bastilion(host,flags.bastilion_username,flags.bastilion_password)