iimport subprocess
import sys
import argparse
import ctypes

# Banner displayed only once at startup
BANNER = """
                        | 
    ____________    __ -+-  ____________ 
    \_____     /   /_ \ |   \     _____/
      \_____    \____/  \____/    _____/
        \_____                    _____/
           \___________  ___________/
                      /____\

   ___                     _   _            _     _ _ _ 
  / _ \ _ __   ___ _ __   | |_| |__   ___  | |__ (_) | |
 | | | | '_ \ / _ \ '_ \  | __| '_ \ / _ \ | '_ \| | | |
 | |_| | |_) |  __/ | | | | |_| | | |  __/ | |_) | | | |
  \___/| .__/ \___|_| |_|  \__|_| |_|\___| |_.__/|_|_|_|
  __ _|_|_ _| |_ ___  ___  | |_ ___   | |__   ___| | | 
 / _` |/ _` | __/ _ \/ __| | __/ _ \  | '_ \ / _ \ | | 
| (_| | (_| | ||  __/\__ \ | || (_) | | | | |  __/ | | 
 \__, |\__,_|\__\___||___/  \__\___/  |_| |_|\___|_|_| 
 |___/ 

 Script by: Thijs, Mario, Laurens
"""

def is_admin():
    """Check if script is running with administrator privileges."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def check_defender_status():
    """Check if Windows Defender is enabled."""
    cmd = "powershell Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        status = result.stdout.strip()
        if status == "True":
            print("Windows Defender is already disabled.")
        else:
            print("Windows Defender is enabled.")
    else:
        print("Error checking Defender status:", result.stderr)

def disable_defender():
    """Disable Windows Defender real-time protection."""
    if not is_admin():
        print("Error: This script must be run as an administrator!")
        return

    try:
        cmd = "powershell -Command \"Set-MpPreference -DisableRealtimeMonitoring $true\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Windows Defender has been disabled successfully.")
        else:
            print("Failed to disable Windows Defender:", result.stderr)
    except Exception as e:
        print("An error occurred:", str(e))

def show_help():
    """Display help options."""
    help_text = """
    Available options:
    --help      Show this help menu
    --status    Check Windows Defender status
    --disable   Disable Windows Defender real-time protection
    """
    print(help_text)

def main():
    """Main function to parse arguments and run commands."""
    print(BANNER)  # Print banner once at startup

    parser = argparse.ArgumentParser(description="Windows Defender Control Script")
    parser.add_argument("--status", action="store_true", help="Check Defender status")
    parser.add_argument("--disable", action="store_true", help="Disable Defender")
    
    args = parser.parse_args()

    if args.status:
        check_defender_status()
    elif args.disable:
        disable_defender()
    else:
        show_help()

if __name__ == "__main__":
    main()

