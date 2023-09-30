import os
import time

os.system('python3 copy_ssh_local.py')
time.sleep(5)
os.system('docker compose up')
print('Docker image created successfully.')