import os
import sys

name = sys.argv[1]
os.system(f'adduser --disabled-password --gecos GECOS {name} && sudo su - {name} && mkdir .ssh/')
os.chmod(f'/home/{name}/.ssh/authorized_keys', 600)
os.chmod(f'/home/{name}/.ssh', 700)