import paramiko
import os
from decouple import config

# Define your SSH server details
ssh_host = config("HOSTNAME")
ssh_port = int(config("PORT"))
ssh_username = config("USER_NAME")
ssh_password = config("PASSWORD")

# Local directory path
local_dir = ""

# Remote directory path on the SSH server
remote_dir = "./"

# List of files to upload
files_to_upload = ["kkkk.txt"]

# Create an SSH client
ssh_client = paramiko.SSHClient()

# Automatically add the server's host key (this is insecure and should be handled differently in production)
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the SSH server
    ssh_client.connect(ssh_host, ssh_port, ssh_username, ssh_password)

    # Create an SFTP client
    sftp = ssh_client.open_sftp()

    # Change to the remote directory (create it if it doesn't exist)
    try:
        sftp.chdir(remote_dir)
    except IOError:
        sftp.mkdir(remote_dir)
        sftp.chdir(remote_dir)

    # Upload each file to the remote directory
    for file_name in files_to_upload:
        local_path = os.path.join(local_dir, file_name)
        remote_path = os.path.join(remote_dir, file_name)
        sftp.put(local_path, remote_path)
        print(f"Uploaded {file_name} to {ssh_host}:{remote_path}")

    # Close the SFTP session and SSH connection
    sftp.close()
    ssh_client.close()

except paramiko.AuthenticationException:
    print("Authentication failed")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
