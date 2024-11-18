import platform
import sys

def run_platform_script():
    system_platform = platform.system().lower()

    if system_platform == 'windows':
        import windows_script
        windows_script.run()
    elif system_platform == 'darwin':  # macOS is identified as 'darwin'
        import macos_script
        macos_script.run()
    else:
        print(f"Unsupported platform: {system_platform}")
        sys.exit(1)

if __name__ == "__main__":
    run_platform_script()
def run():
    print("Running Windows-specific logic.")
    # Add any Windows-specific code here
def run():
    print("Running macOS-specific logic.")
    # Add any macOS-specific code here
def shared_function():
    print("This function can be used across all platforms.")
    # Add any shared logic here
