import os
import paramiko
import stat

# SFTP Connection Details
host = "my_ip_address"
port = 22
username = "Mechachleopteryx"
password = "my_password"
remote_path = "OneDrive/Documents/Github/stuff"
local_path = os.getcwd()


def download_recursive(sftp, remote_path, local_path):
    """
    Recursively download files from the remote directory to the local directory.
    """
    try:
        items = sftp.listdir_attr(remote_path)
        for item in items:
            remote_item_path = os.path.join(remote_path, item.filename)
            local_item_path = os.path.join(local_path, item.filename)

            if stat.S_ISDIR(item.st_mode):
                # If it's a directory, create it locally and recurse into it
                if not os.path.exists(local_item_path):
                    os.makedirs(local_item_path)
                download_recursive(sftp, remote_item_path, local_item_path)
            else:
                # If it's a file, download it if not already present locally
                if not os.path.exists(local_item_path):
                    print(f"Downloading {remote_item_path}...")
                    sftp.get(remote_item_path, local_item_path)
                else:
                    print(f"{local_item_path} already exists locally. Skipping...")
    except FileNotFoundError:
        print(f"Error: Remote path '{remote_path}' does not exist.")
    except Exception as e:
        print(f"Unexpected error during recursive download: {e}")

try:
    # Connect to SFTP Server
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    try:
        print(f"Starting recursive download from remote path: {remote_path}")
        download_recursive(sftp, remote_path, local_path)

    finally:
        # Close the SFTP connection
        sftp.close()
        print("SFTP connection closed.")

except paramiko.ssh_exception.SSHException as e:
    print(f"SSH error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'transport' in locals():
        transport.close()
        print("Transport connection closed.")