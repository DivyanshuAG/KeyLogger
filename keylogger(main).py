import platform
import sys

def run_platform_script():
    system_platform = platform.system().lower()

    if system_platform == 'windows':
        import windows_script
        windows_script.run()
    elif system_platform == 'darwin':
        import macos_script
        macos_script.run()
    else:
        print(f"Unsupported platform: {system_platform}")
        sys.exit(1)

if name== "main":
    run_platform_script()
def run():
    print("Running Windows-specific logic.")
def run():
    print("Running macOS-specific logic.")
def shared_function():
    print("This function can be used across all platforms.")
    
