# knowledge_base.py
# ----------------------------------------------------------
# This file is the "Knowledge Base" used by the RAG (Retrieval
# Augmented Generation) part of the AI IT Helpdesk Agent.
#
# Each entry has:
#   id       -> unique identifier
#   issue    -> short title of the problem
#   keywords -> words the agent uses to match user's question
#   solution -> the troubleshooting steps to show the user
#   severity -> "low", "medium", "high" (used by the Agent to
#               decide whether to auto-resolve or raise a ticket)
# ----------------------------------------------------------

KNOWLEDGE_BASE = [
    {
        "id": "KB001",
        "issue": "Wi-Fi / Internet not connecting",
        "keywords": ["wifi", "wi-fi", "internet", "network", "connect",
                      "disconnect", "no internet", "lan"],
        "solution": [
            "Restart your Wi-Fi router / modem (unplug for 10 seconds).",
            "Forget the Wi-Fi network on your laptop and reconnect.",
            "Run 'ipconfig /release' then 'ipconfig /renew' (Windows) "
            "or toggle Wi-Fi off/on (Mac/Linux).",
            "Check if other devices can connect - if not, contact ISP."
        ],
        "severity": "low"
    },
    {
        "id": "KB002",
        "issue": "Laptop / System running very slow",
        "keywords": ["slow", "lag", "hang", "freeze", "performance",
                      "not responding", "stuck"],
        "solution": [
            "Close unused background applications and browser tabs.",
            "Check Task Manager / Activity Monitor for high CPU/RAM usage.",
            "Clear temporary files (Disk Cleanup / CleanMyMac).",
            "Restart the system to clear memory leaks.",
            "Run a malware/antivirus scan."
        ],
        "severity": "medium"
    },
    {
        "id": "KB003",
        "issue": "Forgot password / cannot login",
        "keywords": ["password", "login", "log in", "locked out",
                     "forgot password", "reset password", "account locked"],
        "solution": [
            "Use the 'Forgot Password' link on the login page.",
            "Check for a password-reset email (also check spam folder).",
            "Ensure Caps Lock is off while typing the password.",
            "If account is locked after failed attempts, wait 15 minutes "
            "or contact admin to unlock it."
        ],
        "severity": "low"
    },
    {
        "id": "KB004",
        "issue": "Printer not printing",
        "keywords": ["printer", "print", "printing", "paper jam",
                     "no output"],
        "solution": [
            "Check the printer is powered on and connected (USB/Wi-Fi).",
            "Ensure the correct printer is selected as default.",
            "Clear the print queue and try printing again.",
            "Reinstall / update the printer driver."
        ],
        "severity": "low"
    },
    {
        "id": "KB005",
        "issue": "Blue screen / System crash",
        "keywords": ["blue screen", "bsod", "crash", "crashed",
                     "system error", "restart automatically"],
        "solution": [
            "Note down the error code shown on the blue screen.",
            "Boot into Safe Mode and uninstall recently added drivers/apps.",
            "Run 'sfc /scannow' to repair corrupted system files.",
            "Update Windows and all device drivers.",
            "If it persists, this is a hardware-level issue - escalate to L2 support."
        ],
        "severity": "high"
    },
    {
        "id": "KB006",
        "issue": "Software installation failing",
        "keywords": ["install", "installation", "setup failed",
                     "cannot install", "error installing"],
        "solution": [
            "Run the installer as Administrator.",
            "Temporarily disable antivirus during installation.",
            "Ensure enough free disk space is available.",
            "Download the installer again in case the file is corrupted."
        ],
        "severity": "medium"
    },
    {
        "id": "KB007",
        "issue": "Email not sending or receiving",
        "keywords": ["email", "mail", "outlook", "gmail", "not sending",
                     "not receiving"],
        "solution": [
            "Check your internet connection.",
            "Verify email server settings (IMAP/SMTP) are correct.",
            "Check if mailbox storage is full.",
            "Clear the 'Outbox' folder of stuck emails and resend."
        ],
        "severity": "low"
    },
    {
        "id": "KB008",
        "issue": "VPN not connecting",
        "keywords": ["vpn", "remote access", "cannot connect vpn"],
        "solution": [
            "Check your internet connection is active.",
            "Confirm VPN username/password are correct and not expired.",
            "Restart the VPN client application.",
            "Try switching VPN server location if the current one is down."
        ],
        "severity": "medium"
    },
]
