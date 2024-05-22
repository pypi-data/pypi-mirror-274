import http.server
import platform
import ctypes
import winreg
import sys
import os

__all__ = [
    "__version__", "BasicHTTPServer", "NamedDict", "_get_http_server_handler", "_get_bundle", 
    "_norm_url", "_check_exists",  "_check_is_dir", "_get_path_limit", "_read_file", "_get_path"
]

__version__ = "2.0.1"

SYS_BUNDLE_ATTRIBUTE = "bundled"

class BasicHTTPServer(http.server.SimpleHTTPRequestHandler):
    pass

class NamedDict(dict):
    def __init__(self, iterable):
        for key, value in iterable.items():
            if isinstance(value, dict):
                self[key] = NamedDict(value)
                continue

            self[key] = value

def _get_bundle():
    return getattr(sys, SYS_BUNDLE_ATTRIBUTE, None)

def _get_http_server_handler():
    if _get_bundle() is not None:
        import ralium.bundle
        return ralium.bundle.BundledHTTPServer
    return BasicHTTPServer

def _check_exists(path):
    bundle = _get_bundle()

    if bundle is not None:
        if path in ["\\template", "\\template\\routes"]: return True
        return bundle.get(path, False)
    
    return os.path.exists(path)

def _check_is_dir(path):
    bundle = _get_bundle()

    if bundle is not None:
        return True
    
    return os.path.isdir(path)

def _norm_url(path):
    return os.path.normpath(f"/{path.lstrip('/\\')}").replace("\\", "/")

def _get_path_limit_winreg():
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
        max_path_length, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
        return max_path_length

def _get_path_limit():
    system = platform.system()

    try:
        if system == 'Windows':
            return os.path.getconf('PC_NAME_MAX')
        
        if system == 'Darwin':
            return os.pathconf('/', 'PC_NAME_MAX')

        libc = ctypes.CDLL('libc.so.6')
        return libc.fpathconf('/', 261)
    except:
        if system == "Windows":
            return 32767 if _get_path_limit_winreg() else 255

def _read_file(path, encoding = "UTF-8"):
    bundle = _get_bundle()

    if bundle is not None:
        return bundle[path].decode(encoding)
    
    with open(path, "r", encoding=encoding) as f:
        return f.read()

def _get_path(path):
    bundle = _get_bundle()

    if bundle is not None:
        return os.path.normpath(path)

    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.join(sys._MEIPASS, path))

    return os.path.abspath(path)