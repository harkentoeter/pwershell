import subprocess
import os
from win32security import LogonUserA, LOGON32_PROVIDER, PROP_LOGON, LUID_AND_SID
from ctypes import windll

# Define PowerShell commands to disable Microsoft Defender
disable_cmd = 'Get-MpPreference | Set-MpPreference -DisableRealtimeMonitoring $true'

def disable_defender():
    # If the user is already logged in as admin, run with elevated permissions
    if windll.shell32.IsUserAnAdmin():
        os.execl(sys.executable, sys.executable, "-u", os.path.realpath(__file__), "/c", disable_cmd)
    
def show_help():
    # Print program usage instructions
    print("Usage: disable_defender.py [/help]")
    print("Options:")
    print("- /help: Display this help message")
    print("- Without arguments, the script will prompt for administrator credentials and then disable Microsoft Defender.")

# Check if an argument is provided
if len(sys.argv) > 1:
    arg = sys.argv[1]
    
    # If the argument is '/help', display the help message
    if arg == "/help":
        show_help()
    else:
        disable_defender()
else:
    disable_defender()

