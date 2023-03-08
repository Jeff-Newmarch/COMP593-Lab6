import requests
import hashlib
import subprocess
import os



def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
        sha256_file = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
        resp_msg = requests.get(sha256_file)

        if resp_msg.status_code == requests.codes.ok:
            sha_file_content = resp_msg.text
        
        return sha_file_content

def download_installer():
    installer_file = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(installer_file)
    if resp_msg.status_code == requests.codes.ok:
            file_content = resp_msg.content
    
    return file_content

def installer_ok(installer_data, expected_sha256):
    installer_file = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(installer_file)
    
    sha256_file = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
    expected_sha256 = requests.get(sha256_file)
    
    if resp_msg.ok:
        file_content = resp_msg.content
        installer_data = hashlib.sha256(file_content).hexdigest()
        if expected_sha256 == installer_data:
            return installer_data
    
def save_installer(installer_data):
    for installer_data in installer_ok():
        with open(r'C:\temp\vlc-3.0.17.4-win64.exe', 'wb') as file:
            file.write(installer_data)


def run_installer(installer_path):
    installer_path = r'C:\temp\vlc-3.0.17.4-win64.exe'
    subprocess.run([installer_path, '/L=1033', '/S'])
    
    
def delete_installer(installer_path):
    installer_path = r'C:\temp\vlc-3.0.17.4-win64.exe'
    os.remove(installer_path)
    

if __name__ == '__main__':
    main()