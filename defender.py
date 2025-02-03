import subprocess

def print_banner():
    banner = """
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
    """
    print(banner)
    print("Script by: Thijs, Mario, Laurens\n")

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
    try:
        cmd = "powershell -Command \"Set-MpPreference -DisableRealtimeMonitoring $true\""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Windows Defender has been disabled.")
        else:
            print("Failed to disable Windows Defender:", result.stderr)
    except Exception as e:
        print("An error occurred:", str(e))

def show_help():
    """Display help options."""
    help_text = """
    Available options:
    - /help : Show this help menu
    - /status : Check Windows Defender status
    - /disable : Disable Windows Defender real-time protection
    - /quit : Exit the program
    """
    print(help_text)

if __name__ == "__main__":
    print_banner()
    while True:
        command = input("Enter command (/help for options): ").strip().lower()
        if command == "/help":
            show_help()
        elif command == "/status":
            check_defender_status()
        elif command == "/disable":
            disable_defender()
        elif command == "/quit":
            print("Exiting program...")
            break
        else:
            print("Invalid option. Use /help for a list of commands.")

