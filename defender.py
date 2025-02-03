import subprocess
import os
from ctypes import windll

# Define PowerShell commands to disable Microsoft Defender
disable_cmd = 'Get-MpPreference | Set-MpPreference -DisableRealtimeMonitoring $true'

def is_admin():
    """
    Checks if the current user is an administrator.
    Returns True if the user is an admin, False otherwise.
    """
    try:
        # Use the 'is_admin' command to check if the user has administrator privileges
        is_admin = subprocess.run(['powershell', '-Command', '"& {if ([Security.PrincipalAccessControlServices]::UserIsAdmin($Env:COMPUTERNAME\$env:USERNAME)) {return $true} else {return $false}}"'], check=True, text=True).stdout
        return is_admin == 'True'
    except Exception as e:
        print(f"Error occurred while checking for admin privileges: {e}")
        return False

def disable_defender():
    # If the user is already logged in as admin, run with elevated permissions
    if is_admin():
        os.execl(sys.executable, sys.executable, "-u", os.path.realpath(__file__), "/c", disable_cmd)
    
def show_help():
    # Print program usage instructions
    print("Usage: disable_defender.py [/help]")
    print("Options:")
    print("- /help: Display this help message")
    print("- Without arguments, the script will prompt for administrator credentials and disable Microsoft Defender.")

# Main code execution
if __name__ == "__main__":
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-h", "--help", help="Display help information.", action="store_true")
    args = parser.parse_args()

    if args.help:
        show_help()
    else:
        disable_defender()

