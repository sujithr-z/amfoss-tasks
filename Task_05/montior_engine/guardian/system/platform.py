import platform

def detect_os():
    system = platform.system()
    if system == "Linux":
        return "Linux"
    elif system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    else:
        return "Unknown"