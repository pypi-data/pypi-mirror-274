from ralium.bundle import BundledHTTPServer, FileSystem

from typing import (
    TypeAlias, 
    Callable, 
    TypeVar, 
    Literal,
    Self, 
    Any, 
)

from types import (
    FunctionType, 
    ModuleType
)

import http.server

__all__ = [
    "__version__",
    "BasicHTTPServer", "_get_http_server_handler", "_get_bundle", "_norm_url", "_check_exists", 
    "_check_is_dir", "_get_path_limit", "_read_file", "_get_path", "_is_markup_filelike"
]

__version__: str

_RT = TypeVar("_RT") # Return Type
ClassType: TypeAlias = object
DirPathStr: TypeAlias = str
FilePathStr: TypeAlias = str

class BasicHTTPServer(http.server.SimpleHTTPRequestHandler): ...

def _get_bundle() -> FileSystem | None: ...
def _get_http_server_handler() -> BasicHTTPServer | BundledHTTPServer: ...
def _check_exists(path: str) -> bool: ...
def _check_is_dir(path: str) -> bool: ...
def _norm_url(path: str) -> str: ...
def _get_path_limit_winreg() -> int: ...
def _get_path_limit() -> int: ...
def _read_file(path: str, encoding: str = "UTF-8") -> str: ...
def _get_path(path: str) -> str: ...
def _is_markup_filelike(markup: str) -> bool: ...