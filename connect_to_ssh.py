import paramiko


hostname = ''
port = ''
ssh_client = paramiko.SSHClient()

# Add to known
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Creds
username = ''
password = ''

try:
    # Connect to SSH 
    ssh_client.connect(hostname, port, username, password)

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
