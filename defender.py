import subprocess
import sys
import ctypes

def banner():
    print("""
  ⡟⠋⠉⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⢿⣿
  ⣿⠀⠀⠀⠀⠀⠀⠉⠻⠿⣿⡿⣿⣿⣿⣿⣿⠿⠟⠋⠁⠀⠀⠀⢰⣿
  ⣿⣦⠀⠀⠀⠦⢄⣤⠆⠀⠀⠀⠹⠟⠛⠀⠀⠰⠦⠖⠋⠀⠀⢰⣿⣿
  ⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣶⣦⠀⠀⠀⠀⠀⠀⢠⣶⣾⣿⢿
  ⣿⣿⣿⣿⣦⠀⠀⢀⣠⣤⣾⣿⣿⣿⣿⣿⣵⣶⣦⣤⣶⣾⣿⣿⡟⣼
  ⣷⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢣⣿
  ⣿⣧⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣠⣿⣿
  ⣿⣿⣦⠘⣿⢿⣿⣿⣿⣯⣟⢿⣿⣿⣿⢿⣿⣿⣿⣿⠿⠇⣴⣿⣿⣿
  ⣿⣿⣿⣷⡄⠘⠛⠛⣿⣿⣿⣿⣶⣿⣶⣿⣿⠟⠋⠀⠀⣸⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⣤⣶⣿⣿⣿⣿⣿⣿
  ⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣀⣀⣀⣀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿

    Thijs | Laurens | Mario
    =======================================
    """)

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    if not is_admin():
        print("[*] Administratorrechten worden aangevraagd...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def disable_defender():
    print("[*] Proberen Windows Defender real-time bescherming uit te schakelen...")
    try:
        subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", 
            "Set-MpPreference -DisableRealtimeMonitoring $true"
        ], shell=True, check=True, capture_output=True, text=True)
        print("[+] Windows Defender real-time bescherming is uitgeschakeld.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Fout bij uitschakelen Defender: {e.stderr}")

def check_defender_status():
    print("[*] Controleren of Windows Defender real-time bescherming is uitgeschakeld...")
    try:
        result = subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", 
            "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"
        ], shell=True, capture_output=True, text=True)
        status = result.stdout.strip()
        if status == "True":
            print("[+] Windows Defender real-time bescherming is UIT.")
        else:
            print("[!] Windows Defender real-time bescherming is nog AAN. Controleer of Tamper Protection is uitgeschakeld.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Fout bij controleren Defender status: {e.stderr}")

def show_help():
    print("\nGebruik: python script.py [optie]\n")
    print("Beschikbare opties:")
    print("  /disable   - Schakel Windows Defender real-time bescherming uit")
    print("  /help      - Toon deze helptekst")
    sys.exit()

def main():
    banner()
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "/help":
            show_help()
        elif sys.argv[1].lower() == "/disable":
            run_as_admin()
            disable_defender()
            check_defender_status()
        else:
            print("[!] Ongeldige optie. Gebruik '/help' voor hulp.")
            sys.exit()
    else:
        print("[!] Geen optie opgegeven. Gebruik '/help' voor hulp.")
        sys.exit()

if __name__ == "__main__":
    main()

