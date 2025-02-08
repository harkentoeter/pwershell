import sys
import os
import subprocess
import ctypes
import argparse
import logging
import shutil
from datetime import datetime

# Define PowerShell Path explicitly
POWERSHELL_PATH = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

# Ensure log file is written to the correct directory (for .exe compatibility)
LOG_FILE = os.path.join(os.path.dirname(sys.executable), "defender.log") if getattr(sys, 'frozen', False) else "defender.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s UTC %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_admin():
    """Check if the script is running as administrator."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    """Relaunch the script with administrator privileges if not already elevated."""
    if not is_admin():
        logger.info("Requesting administrator privileges...")
        try:
            exe = sys.executable
            params = " ".join(f'"{arg}"' for arg in sys.argv)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
            os._exit(0)  # Force exit to allow elevation
        except Exception as e:
            logger.error(f"Failed to relaunch with admin privileges: {e}")
            sys.exit(1)

def run_powershell(command):
    """Run a PowerShell command securely and return the output or handle errors."""
    try:
        result = subprocess.run(
            [POWERSHELL_PATH, '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        logger.info(f"Command executed: {command} with output: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown PowerShell error."
        logger.error(f"PowerShell error: {error_msg}")
        print(f"PowerShell error: {error_msg}")
        if "execution policy" in error_msg.lower():
            print("Try running: Set-ExecutionPolicy RemoteSigned")
        elif "tamper protection" in error_msg.lower():
            print("Tamper Protection is enabled; disable it manually.")
        sys.exit(1)

def check_tamper_protection():
    """Check if Windows Defender Tamper Protection is enabled."""
    logger.info("Checking Tamper Protection status...")
    command = "(Get-MpPreference).EnableTamperProtection"
    output = run_powershell(command)
    if output.strip() == "True":
        print("Tamper Protection is enabled. You must disable it manually before proceeding.")
        logger.warning("Tamper Protection is enabled. Script cannot modify Defender settings.")
        sys.exit(1)
    else:
        logger.info("Tamper Protection is disabled. Proceeding with Defender modification.")

def check_status():
    """Check if Windows Defender is running."""
    logger.info("Checking Windows Defender status...")
    try:
        result = subprocess.run(['sc', 'query', 'Windefend'], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if "RUNNING" in output:
            print("Windows Defender is running.")
            logger.info("Windows Defender is running.")
        elif "STOPPED" in output:
            print("Windows Defender is stopped.")
            logger.info("Windows Defender is stopped.")
        else:
            print("Defender status unknown.")
            logger.warning("Defender status unknown.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking status: {e}")
        print(f"Error checking status: {e}")

def disable_defender(dry_run=False):
    """Disable Windows Defender real-time protection."""
    command = "Set-MpPreference -DisableRealtimeMonitoring $true"
    if dry_run:
        print(f"Dry run: {command}")
        logger.info(f"Dry run: {command}")
    else:
        check_tamper_protection()  # Ensure Tamper Protection is off before modifying Defender
        logger.info(f"Disabling Windows Defender real-time protection using command: {command}")
        run_powershell(command)
        print("Windows Defender real-time protection disabled.")

def enable_defender(dry_run=False):
    """Enable Windows Defender real-time protection."""
    command = "Set-MpPreference -DisableRealtimeMonitoring $false"
    if dry_run:
        print(f"Dry run: {command}")
        logger.info(f"Dry run: {command}")
    else:
        logger.info(f"Enabling Windows Defender real-time protection using command: {command}")
        run_powershell(command)
        print("Windows Defender real-time protection enabled.")

def main():
    """Main function to handle arguments and execute commands."""
    parser = argparse.ArgumentParser(description='Manage Windows Defender.')
    parser.add_argument('--disable', action='store_true', help='Disable Windows Defender.')
    parser.add_argument('--enable', action='store_true', help='Enable Windows Defender.')
    parser.add_argument('--check-status', action='store_true', help='Check the current status of Windows Defender.')
    parser.add_argument('--dry-run', action='store_true', help='Show commands without executing.')
    args = parser.parse_args()

    # Ensure the script runs with admin privileges
    run_as_admin()

    if args.dry_run:
        logger.info("Dry run mode activated. No changes will be made.")
        if args.check_status:
            check_status()
        if args.disable:
            disable_defender(dry_run=True)
        if args.enable:
            enable_defender(dry_run=True)
        sys.exit(0)

    if args.check_status:
        check_status()
    elif args.disable:
        disable_defender()
    elif args.enable:
        enable_defender()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

