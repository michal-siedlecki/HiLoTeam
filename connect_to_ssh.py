import paramiko
from decouple import config

# Creds
username = config('USER_NAME')
password = config('PASSWORD')
private_key = ''
hostname = config('HOSTNAME')
port = int(config('PORT'))

ssh_client = paramiko.SSHClient()

# Add to known
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to SSH
    if not private_key:
        ssh_client.connect(hostname, port, username, password)
    else:
        ssh_client.connect(hostname, username=username, key_filename=private_key)

    # Do something
    command = 'cat asdf.txt'
    stdin, stdout, stderr = ssh_client.exec_command(command)

    # Print command output
    print("Command output:")
    for line in stdout:
        print(line.strip())

    # Close ssh connection
    ssh_client.close()

# Catch exceptions
except paramiko.AuthenticationException as auth_error:
    print(f"Authentication failed: {auth_error}")
except paramiko.SSHException as ssh_error:
    print(f"SSH connection error: {ssh_error}")
except Exception as e:
    print(f"An error occurred: {e}")
