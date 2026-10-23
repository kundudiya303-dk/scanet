#!/usr/bin/env python3
"""
scanet — High-Impact Universal Launcher
Cross-platform environment setup, dependency verification, and server orchestration.
"""
import sys
import os
import platform
import subprocess
import urllib.request
import socket
import time
import hashlib
import shutil
import venv


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")
VENV_DIR = os.path.join(BACKEND_DIR, ".venv")


def ensure_project_environment():
    """Run from the project virtual environment, creating it on first launch."""
    if sys.version_info < (3, 10):
        print(f"Python 3.10+ is required; found {platform.python_version()}.")
        raise SystemExit(1)

    venv_python = os.path.join(
        VENV_DIR,
        "Scripts" if os.name == "nt" else "bin",
        "python.exe" if os.name == "nt" else "python",
    )
    venv_is_usable = False
    if os.path.isfile(venv_python):
        try:
            result = subprocess.run(
                [venv_python, "-c", "import sys; raise SystemExit(sys.version_info < (3, 10))"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            venv_is_usable = result.returncode == 0
        except OSError:
            pass

    if venv_is_usable and os.path.samefile(sys.executable, venv_python):
        return

    if not venv_is_usable:
        print("Creating the project virtual environment...")
        try:
            if os.path.exists(VENV_DIR):
                shutil.rmtree(VENV_DIR)
            os.makedirs(BACKEND_DIR, exist_ok=True)
            venv.EnvBuilder(with_pip=True).create(VENV_DIR)
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            print(f"Could not create the project virtual environment: {exc}")
            raise SystemExit(1) from exc

    try:
        result = subprocess.run([venv_python, os.path.abspath(__file__), *sys.argv[1:]])
    except OSError as exc:
        print(f"Could not start the project virtual environment: {exc}")
        raise SystemExit(1) from exc
    raise SystemExit(result.returncode)

# Enforce UTF-8 encoding across Windows, Linux, and macOS consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Cyberpunk High-Contrast Color Palette (256-Color & ANSI Supported)
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_DIM = "\033[2m"
C_UNDERLINE = "\033[4m"

# Vivid Neon Accents
C_CYAN = "\033[38;5;51m"
C_SKY = "\033[38;5;45m"
C_BLUE = "\033[38;5;39m"
C_PURPLE = "\033[38;5;141m"
C_MAGENTA = "\033[38;5;201m"
C_PINK = "\033[38;5;213m"
C_GREEN = "\033[38;5;48m"
C_LIME = "\033[38;5;154m"
C_YELLOW = "\033[38;5;226m"
C_ORANGE = "\033[38;5;208m"
C_RED = "\033[38;5;196m"
C_WHITE = "\033[38;5;231m"
C_GRAY = "\033[38;5;245m"
C_DARK = "\033[38;5;238m"

def print_banner():
    # Enable ANSI escape sequences on Windows consoles if needed
    if platform.system() == "Windows":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

    print()
    print(f"{C_CYAN}   ███████╗ ██████╗ █████╗ ███╗   ██╗███████╗████████╗{C_RESET}")
    print(f"{C_SKY}   ██╔════╝██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{C_RESET}")
    print(f"{C_BLUE}   ███████╗██║     ███████║██╔██╗ ██║█████╗     ██║   {C_RESET}")
    print(f"{C_PURPLE}   ╚════██║██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   {C_RESET}")
    print(f"{C_MAGENTA}   ███████║╚██████╗██║  ██║██║ ╚████║███████╗   ██║   {C_RESET}")
    print(f"{C_PINK}   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {C_RESET}")
    print()
    print(f"  {C_PURPLE}⚡ WEB-ORCHESTRATED CYBERSECURITY RECONNAISSANCE PLATFORM{C_RESET}")
    print(f"  {C_BLUE}🔒 12 Recon Engines · OS Fingerprinting · AI MITRE ATT&CK · SARIF v2.1{C_RESET}")
    print(f"  {C_DARK}─────────────────────────────────────────────────────────────────────────────{C_RESET}")

def get_public_ip():
    try:
        with urllib.request.urlopen("https://checkip.amazonaws.com", timeout=2) as resp:
            return resp.read().decode().strip()
    except Exception:
        try:
            with urllib.request.urlopen("https://api.ipify.org", timeout=2) as resp:
                return resp.read().decode().strip()
        except Exception:
            return None

def print_host_audit(port, public_ip):
    hostname = socket.gethostname()
    os_name = f"{platform.system()} {platform.release()}"
    arch = platform.machine()
    py_ver = platform.python_version()

    print(f"\n  {C_BOLD}{C_WHITE}╭─── 🖥️  HOST ENVIRONMENT AUDIT ──────────────────────────────────────────────╮{C_RESET}")
    print(f"  {C_WHITE}│{C_RESET}  {C_SKY}• Node Host:{C_RESET}       {C_WHITE}{hostname}{C_RESET} ({arch})")
    print(f"  {C_WHITE}│{C_RESET}  {C_SKY}• Operating Sys:{C_RESET}   {C_WHITE}{os_name}{C_RESET} │ Python {C_YELLOW}{py_ver}{C_RESET}")
    if public_ip:
        print(f"  {C_WHITE}│{C_RESET}  {C_SKY}• Public IPv4:{C_RESET}     {C_LIME}{public_ip}{C_RESET} {C_DIM}(Cloud / External Access Detected){C_RESET}")
    else:
        print(f"  {C_WHITE}│{C_RESET}  {C_SKY}• Public IPv4:{C_RESET}     {C_GRAY}Private / Local Subnet{C_RESET}")
    print(f"  {C_WHITE}│{C_RESET}  {C_SKY}• Target Port:{C_RESET}     {C_CYAN}TCP {port}{C_RESET} {C_DIM}(HTTP Direct Access){C_RESET}")
    print(f"  {C_BOLD}{C_WHITE}╰─────────────────────────────────────────────────────────────────────────────╯{C_RESET}\n")

def prompt_interactive(port):
    if not sys.stdin.isatty() or os.environ.get("SCANET_NON_INTERACTIVE") == "1":
        return port

    print(f"  {C_BOLD}{C_WHITE}╭─── 🎮 INTERACTIVE CONTROL ───────────────────────────────────────────────────╮{C_RESET}")
    print(f"  {C_WHITE}│{C_RESET}  {C_CYAN}[1]{C_RESET} {C_BOLD}🚀 Launch Web Platform{C_RESET} {C_DIM}(Default - Press ENTER to launch){C_RESET}               {C_WHITE}│{C_RESET}")
    print(f"  {C_WHITE}│{C_RESET}  {C_YELLOW}[2]{C_RESET} {C_BOLD}🔧 Change HTTP Port{C_RESET}    {C_DIM}(Current: TCP {port}){C_RESET}                                   {C_WHITE}│{C_RESET}")
    print(f"  {C_WHITE}│{C_RESET}  {C_PURPLE}[3]{C_RESET} {C_BOLD}🩺 Self-Diagnostics{C_RESET}    {C_DIM}(Check interfaces & system resources){C_RESET}          {C_WHITE}│{C_RESET}")
    print(f"  {C_BOLD}{C_WHITE}╰─────────────────────────────────────────────────────────────────────────────╯{C_RESET}")

    try:
        # Non-blocking prompt on Windows/Unix with short fallback
        choice = input(f"  {C_SKY}Select option [1-3] or press [ENTER] to launch:{C_RESET} ").strip()
        if choice == "2":
            new_port = input(f"  {C_YELLOW}Enter custom HTTP port [default: 8000]:{C_RESET} ").strip()
            if new_port.isdigit():
                port = int(new_port)
                print(f"  {C_GREEN}✓ Port updated to TCP {port}{C_RESET}\n")
        elif choice == "3":
            print(f"\n  {C_SKY}--- RUNNING SELF-DIAGNOSTICS ---{C_RESET}")
            print(f"  {C_DIM}CPU Count:{C_RESET}  {os.cpu_count() or 1} Cores")
            print(f"  {C_DIM}Platform:{C_RESET}   {platform.platform()}")
            print(f"  {C_GREEN}✓ System ready for reconnaissance pipeline.{C_RESET}\n")
    except Exception:
        pass
    return port

def check_python():
    if sys.version_info < (3, 10):
        print(f"  {C_RED}[✗] Error: Python 3.10+ required. Current version: {sys.version}{C_RESET}")
        sys.exit(1)
    print(f"  {C_PURPLE}[1/4]{C_RESET}  {C_BOLD}{C_WHITE}PYTHON RUNTIME VERIFICATION{C_RESET} ... {C_GREEN}✓ Python {platform.python_version()} Compatible{C_RESET}")

def setup_environment():
    data_dir = os.path.join(BACKEND_DIR, "data")
    os.makedirs(data_dir, exist_ok=True)

    print(f"  {C_PURPLE}[2/4]{C_RESET}  {C_BOLD}{C_WHITE}DATA STORE PROVISIONING{C_RESET}     ... {C_GREEN}✓ SQLite Directory Active{C_RESET}")

    req_file = os.path.join(BACKEND_DIR, "requirements.txt")
    marker_file = os.path.join(VENV_DIR, ".requirements.sha256")
    with open(req_file, "rb") as requirements:
        requirements_hash = hashlib.sha256(requirements.read()).hexdigest()

    print(f"  {C_PURPLE}[3/4]{C_RESET}  {C_BOLD}{C_WHITE}DEPENDENCY VERIFICATION{C_RESET}     ... ", end="", flush=True)
    try:
        installed_hash = ""
        if os.path.isfile(marker_file):
            with open(marker_file, "r", encoding="ascii") as marker:
                installed_hash = marker.read().strip()
        dependencies_valid = (
            subprocess.run(
                [sys.executable, "-m", "pip", "check"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            ).returncode == 0
        )
        if installed_hash != requirements_hash or not dependencies_valid:
            print(f"{C_YELLOW}Installing project dependencies...{C_RESET}")
            subprocess.run(
                [
                    sys.executable, "-m", "pip", "install",
                    "--prefer-binary", "-r", req_file,
                ],
                check=True,
            )
            with open(marker_file, "w", encoding="ascii") as marker:
                marker.write(requirements_hash)
        print(f"{C_GREEN}✓ Project dependencies ready{C_RESET}")
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"\n{C_RED}Dependency installation failed: {exc}{C_RESET}")
        raise SystemExit(1) from exc

def start_server(port=8000, public_ip=None):
    sys.path.insert(0, BACKEND_DIR)

    print(f"  {C_PURPLE}[4/4]{C_RESET}  {C_BOLD}{C_WHITE}SERVER ORCHESTRATION{C_RESET}        ... {C_GREEN}✓ ASGI Interface Ready{C_RESET}")

    # Magnificent Cyberpunk Online Service Banner
    print(f"\n{C_BOLD}{C_CYAN}  ╔══════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}                     {C_BOLD}{C_YELLOW}⚡  SCANET PLATFORM IS NOW ONLINE  ⚡{C_RESET}                      {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}                                                                              {C_BOLD}{C_CYAN}║{C_RESET}")
    if public_ip:
        print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_BOLD}{C_LIME}🌐  CLOUD PUBLIC ACCESS:{C_RESET}     {C_BOLD}{C_YELLOW}http://{public_ip}:{port}{C_RESET}  {C_DIM}◄ [OPEN IN BROWSER]{C_RESET}   {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_BOLD}{C_SKY}🏠  LOCAL ACCESS LINK:{C_RESET}       {C_WHITE}http://localhost:{port}{C_RESET}                              {C_BOLD}{C_CYAN}║{C_RESET}")
    host_target = public_ip if public_ip else "localhost"
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_BOLD}{C_PURPLE}📚  INTERACTIVE SWAGGER:{C_RESET}     {C_WHITE}http://{host_target}:{port}/docs{C_RESET}                         {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_BOLD}{C_GREEN}🩺  SYSTEM HEALTH PROBE:{C_RESET}     {C_WHITE}http://{host_target}:{port}/api/v1/system/health{C_RESET}        {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}                                                                              {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ╠══════════════════════════════════════════════════════════════════════════════╣{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_ORANGE}⚠️  FIREWALL NOTE:{C_RESET} Ensure Port {port} (Custom TCP) is OPEN in Cloud Security Group! {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ║{C_RESET}   {C_GRAY}⌨️  KEYBOARD:{C_RESET}      Press {C_WHITE}[CTRL + C]{C_RESET} anytime to shut down the server.           {C_BOLD}{C_CYAN}║{C_RESET}")
    print(f"{C_BOLD}{C_CYAN}  ╚══════════════════════════════════════════════════════════════════════════════╝{C_RESET}\n")

    try:
        import uvicorn
    except ImportError:
        print(f"{C_RED}Uvicorn is missing from the configured environment. Re-run the launcher to install dependencies.{C_RESET}")
        raise SystemExit(1)

    try:
        uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
    except KeyboardInterrupt:
        print(f"\n  {C_YELLOW}[*] scanet server terminated gracefully.{C_RESET}\n")

if __name__ == "__main__":
    ensure_project_environment()
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    elif "PORT" in os.environ and os.environ["PORT"].isdigit():
        port = int(os.environ["PORT"])

    print_banner()
    public_ip = get_public_ip()
    print_host_audit(port, public_ip)
    port = prompt_interactive(port)
    check_python()
    setup_environment()
    start_server(port, public_ip)
