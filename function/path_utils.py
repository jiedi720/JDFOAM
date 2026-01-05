"""路径转换工具模块"""


def to_wsl_path(win_path):
    """
    将 Windows 路径转换为 WSL 路径
    
    Args:
        win_path: Windows 路径
        
    Returns:
        str: WSL 路径
    """
    path = win_path.replace('\\', '/')
    if ':' in path:
        drive, rest = path.split(':', 1)
        return f"/mnt/{drive.lower()}{rest}"
    return path