import paramiko
from decouple import config

# Creds
hostname = config("HOSTNAME")
port = int(config("PORT"))
username = config("USER_NAME")
password = config("PASSWORD")

# Initialize client
client = paramiko.SSHClient()
client.load_system_host_keys()

# Connect to SSH
client.connect(hostname, port, username, password)

# File path in SSH
remote_file_path = "docker-compose.yml"

# File path to save file
local_folder_path = ""

# Downloading file
sftp = client.open_sftp()
sftp.get(remote_file_path, local_folder_path + "docker-compose.yml")
sftp.close()

# Close SSH connection
client.close()
