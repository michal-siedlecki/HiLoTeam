import os

# Create dir /keys in current dir
os.system("mkdir keys")

# Command to run, create pair ssh in keys/dir - NO PASSWORD
command = "ssh-keygen -t ECDSA -N '' -f ./keys/ssh_id"

# Execute command, create keys
os.system(command)
