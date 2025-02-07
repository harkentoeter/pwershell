import subprocess
import sys
import ctypes

# PowerShell command to disable Microsoft Defender's real-time monitoring
disable_cmd = [
    "powershell",
    "-ExecutionPolicy", "Bypass",
    "-NoProfile",
    "-Command",
    "Set-MpPreference -DisableRealtimeMonitoring $true"
]

# PowerShell command to check Defender status
check_status_cmd = [
    "powershell",
    "-ExecutionPolicy", "Bypass",
    "-NoProfile",
    "-Command",
    "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"
]

def is_admin():
    """
    Checks if the script is running as administrator.
    Returns True if running as admin, otherwise False.
    """
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    """
    Relaunches the script with administrator privileges if not already elevated.
    """
    if not is_admin():
        print("[*] Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def disable_defender():
    """
    Disables Microsoft Defender using PowerShell.
    """
    print("[*] Attempting to disable Microsoft Defender real-time protection...")

    try:
        subprocess.run(disable_cmd, shell=True, check=True, capture_output=True, text=True)
        print("[+] Defender real-time protection should now be disabled.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to disable Defender: {e.stderr}")

def check_defender_status():
    """
    Checks if Defender real-time protection is disabled.
    """
    print("[*] Checking if Defender real-time protection is disabled...")

    try:
        result = subprocess.run(check_status_cmd, shell=True, capture_output=True, text=True)
        status = result.stdout.strip()

        if status == "True":
            print("[+] Defender real-time protection is OFF.")
        else:
            print("[!] Defender real-time protection is still ON. You may need to disable Tamper Protection.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error checking Defender status: {e.stderr}")

def main():
    """
    Main execution function.
    """
    run_as_admin()  # Ensure script runs as administrator
    disable_defender()
    check_defender_status()
    input("\nPress Enter to exit...")  # Keeps window open

if __name__ == "__main__":
    main()

