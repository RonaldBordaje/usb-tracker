# Enhanced USB Tracker

A Python-based security monitoring tool designed for comprehensive system information collection and notification. Originally created for USB device security studies, this tool gathers detailed device data and sends it via encrypted email alerts.

## ⚠️ DISCLAIMER
**This tool is for EDUCATIONAL PURPOSES ONLY.** Use only on systems you own or have explicit permission to monitor. The developers assume no responsibility for misuse.

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security Features](#security-features)
- [Platform Support](#platform-support)
- [Ethical Guidelines](#ethical-guidelines)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features
- **Comprehensive System Information Collection**
  - Computer name and username
  - Operating system details
  - MAC address and network interfaces
  - Public and local IP addresses
  - Current directory and timestamp

- **Process Monitoring** (Optional)
  - Real-time monitoring of running processes
  - Tracks top 20 memory-consuming processes
  - Requires `psutil` package

- **WiFi Network Scanner**
  - Scans saved WiFi profiles (Windows only)
  - Detects currently connected network
  - Cross-platform compatible

- **Browser Information Detection**
  - Detects installed browsers (Chrome, Firefox, Edge, Opera)
  - Identifies default browser
  - Checks common installation paths

### Security Features
- **Encrypted Data Storage**
  - Fernet symmetric encryption (AES-128-CBC)
  - Timestamped log files
  - Local encrypted storage

- **Stealth Mode**
  - Hides console window on Windows
  - Optional configuration

- **Email Notification System**
  - SMTP email alerts (Gmail supported)
  - Formatted system information
  - Retry mechanism

- **Self-Destruct Capability** (Optional)
  - Deletes script after execution
  - Removes generated logs
  - Configurable option

## 📦 Installation

### Prerequisites
- Python 3.6+
- Required packages

### Install Dependencies
```bash
pip install requests psutil cryptography
```

### Optional Packages
- `ctypes` (usually included with Python)
- Standard library modules: `os`, `platform`, `socket`, `uuid`, `datetime`, `smtplib`, `getpass`, `json`, `subprocess`, `time`

## ⚙️ Configuration

### Configuration File
Edit the CONFIG dictionary in the script:

```python
CONFIG = {
    "email_sender": "your_email@gmail.com",     # Sender email
    "email_password": "app_password",           # Gmail app password
    "email_receiver": "recipient@gmail.com",    # Recipient email
    "smtp_server": "smtp.gmail.com",            # SMTP server
    "smtp_port": 587,                           # SMTP port
    "max_retries": 3,                           # Email retry attempts
    "retry_delay": 5,                           # Delay between retries (seconds)
    "stealth_mode": True,                       # Hide console window
    "save_log": False,                          # Save encrypted log locally
    "self_destruct": False,                     # Delete script after execution
    "encryption_key": b"GENERATE_A_UNIQUE_KEY", # Encryption key
    "monitor_processes": True,                  # Enable process monitoring
    "scan_wifi": True,                          # Enable WiFi scanning
    "browser_check": True                       # Enable browser detection
}
```

### Generating Encryption Key
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(f"Encryption key: {key}")
```

## 🚀 Usage

### Basic Execution
```bash
python usb_tracker.py
```

### Execution Flow
1. **Initialization**: Loads configuration and checks packages
2. **Stealth Mode**: Hides console window if enabled
3. **Data Collection**: Gathers system information
4. **Encryption**: Encrypts collected data (if enabled)
5. **Email Notification**: Sends formatted alert
6. **Cleanup**: Optionally self-destructs

### Command Line Options
*(Add if your script supports them)*

## 🔒 Security Features

### Data Encryption
- Uses Fernet (AES-128-CBC) encryption
- Encrypts all collected data before storage
- Requires unique key for each deployment

### Privacy Protection
- No data sent to external servers (except configured email)
- Optional local log storage
- Configurable data collection

### Secure Email Setup
1. Use Gmail App Passwords (not personal passwords)
2. Enable 2-factor authentication
3. Use secure SMTP (TLS)

## 💻 Platform Support

### Primary Support
- **Windows**: Full feature support including WiFi scanning and stealth mode

### Limited Support
- **Linux/macOS**: Basic features work, but some Windows-specific features are unavailable

## ⚖️ Ethical Guidelines

### Required Practices
1. **Authorization**: Only use on systems you own or have explicit permission
2. **Transparency**: Inform users about monitoring in organizational settings
3. **Data Minimization**: Collect only necessary information
4. **Secure Storage**: Protect collected data with strong encryption
5. **Proper Disposal**: Securely delete data after use

### Legal Compliance
- Check local laws regarding system monitoring
- Obtain necessary permissions
- Maintain audit trails for authorized use
- Respect privacy regulations (GDPR, CCPA, etc.)

## 📁 File Structure

```
usb_tracker.py
├── CONFIG Dictionary                 # Configuration settings
├── get_device_info()                # Main data collection function
├── Feature Functions:
│   ├── get_process_info()           # Process monitoring
│   ├── get_wifi_info()              # WiFi scanning
│   ├── get_browser_info()           # Browser detection
│   ├── encrypt_data()/decrypt_data() # Encryption utilities
│   └── hide_console()               # Stealth mode
├── send_alert()                     # Email notification
└── main()                           # Execution flow
```

## 🐛 Troubleshooting

### Common Issues

**1. Email Not Sending**
```bash
# Check configuration:
- Verify Gmail app password (not personal password)
- Enable "Less Secure Apps" or use app-specific password
- Check internet connectivity
- Verify SMTP settings
```

**2. Missing Features**
```bash
# Install missing packages:
pip install psutil cryptography

# For Windows-specific features:
# Run as Administrator if needed
```

**3. Encryption Errors**
```python
# Generate proper key:
from cryptography.fernet import Fernet
key = Fernet.generate_key()
# Update CONFIG["encryption_key"]
```

**4. Permission Errors**
- Run with appropriate administrator privileges
- Check file/folder permissions
- Verify user account has necessary rights

### Error Handling
The application includes comprehensive error handling:
- Graceful degradation when packages are missing
- Retry mechanisms for email transmission
- Fallback values for failed data collection
- Silent failure for non-critical operations

## 🔧 Customization

### Extending Features
1. **Add new data collection** to `get_device_info()`
2. **Extend platform-specific** implementations
3. **Modify email formatting** in `send_alert()`
4. **Add additional encryption** layers

### Adding New Browsers
Modify the `browsers` dictionary in `get_browser_info()`:
```python
browsers = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    # Add new browsers here
    "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
}
```

## 📧 Email Alert Format

Example email content:
```
System Alert - Device Information

System Information:
- Computer Name: DESKTOP-ABC123
- Username: johndoe
- OS: Windows 10 (10.0.19045)

Network Details:
- MAC Address: 00:1A:2B:3C:4D:5E
- Public IP: 203.0.113.1
- Local IP: 192.168.1.100

Process Monitoring:
Top memory-consuming processes:
1. chrome.exe (1.2GB)
2. code.exe (800MB)

WiFi Information:
- Current SSID: HomeNetwork
- Saved Profiles: HomeNetwork, OfficeWiFi

Browser Detection:
- Chrome: Installed (v120.0.6099.109)
- Firefox: Not found

Timestamp: 2024-01-15 14:30:45
Location: C:\Users\johndoe\Downloads
```

## 📄 License

This project is for educational purposes only. See the [DISCLAIMER](#disclaimer) section.

## 👤 Author

**Ronald Bordaje**  
IT Student  
- GitHub: [@your-username](https://github.com/your-username)

## 🙏 Acknowledgments

- `cryptography` library developers
- `psutil` team for system monitoring capabilities
- Python community for extensive libraries

---

**Remember**: Always use this tool responsibly and legally. Unauthorized monitoring is illegal in most jurisdictions.
