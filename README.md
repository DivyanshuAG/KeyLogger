# Keylogger Project

This repository contains keylogger implementations for both macOS and Windows platforms. The keylogger is designed to monitor user keystrokes, log them to a file, take periodic screenshots, and record system information during its execution. Below is an overview of the keylogger functionality for each platform, as well as some current limitations and ongoing improvements.

---

## Keylogger (macOS)

The **macOS Keylogger** is designed to capture and log keystrokes on macOS systems. Upon termination, the keylogger performs the following actions:

- **Logs the Timestamp**: It records the time at which the keylogger was executed.
- **Takes Screenshots**: A screenshot is captured to visually log the user's screen at the time of execution.
- **Logs Execution Time**: The exact timestamp when the keylogger was running is recorded.
- **Notes the IP address and system information**: The system information is noted and the public ip is also being noted when the keylogger is executed.
**Current Limitations**:
- **Root Permissions**: The keylogger requires root (administrator) permissions to monitor keyboard activity on macOS. This permission request may raise security concerns for the user.
- **Ongoing Improvements**: Efforts are underway to streamline the keylogger's behavior to minimize the need for elevated privileges.

---

## Keylogger (Windows)

The **Windows Keylogger** logs keystrokes on Windows systems, captures screenshots at regular intervals, and employs strategies to conceal activity. Its functionality includes:

- **Keystroke Logging**: Captures all keystrokes made by the user.
- **Regular Screenshots**: Takes periodic screenshots of the user’s screen during the keylogging session.
- **Track Concealment**: To reduce detection, the keylogger deletes keystrokes and screenshots after each iteration, leaving no trace of its activity.

**Current Issues**:
1. **Key Representation**: Some keys, such as `Ctrl`, are logged in hexadecimal format. Efforts to convert these keys into a more human-readable format are still ongoing.
2. **Windows Defender Bypass**: The keylogger may be detected by Windows Defender or other antivirus software. Active development is focused on improving the keylogger's ability to bypass antivirus detection.

---

## Future Improvements
- **Root Permissions**: Ongoing efforts to eliminate the need for elevated privileges (admin/root access) on macOS and Windows.
- **Cross-Platform Compatibility**: Expanding the functionality of the keylogger to support other operating systems like Linux.
- **Enhanced Stealth Mode**: Improving techniques for avoiding antivirus detection and reducing the visibility of the keylogger on the system.

---
