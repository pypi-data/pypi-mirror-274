from ralium.errors import *
from ralium._util import *
import inspect

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
</head>
<body>
</body>
</html>"""

class FileReader:
    def __init__(self, file, encoding):
        self.__data = file
        self.__read = False
        self.__encoding = encoding

        path_length = len(self.__data)
        path_limit = _get_path_limit()

        if path_length > path_limit:
            raise FilePathLimitError(f"Failed to load file, exceeds the max path limit of '{path_limit}'")
        
    @property
    def content(self):
        self._read()
        return self.__data
    
    def _read(self):
        if self.__read:
            return

        if not _check_exists(self.__data):
            return warn(f"Failed to load file with path: '{self.__data}'", FileNotFoundWarning, True)
        
        self.__data = _read_file(_get_path(self.__data), self.__encoding)
        self.__read = True

class CSSReader:
    def __init__(self, *files, encoding):
        self.__readers = []

        for file in files:
            if _check_exists(file):
                if len(file) <= _get_path_limit():
                    warn(f"File '{file}' exceeds path limit.", FilePathLimitWarning, major=True)
                
                self.__readers.append(FileReader(file, encoding))
                continue

            self.__readers.append(file)

    @property
    def content(self):
        items = []
        for reader in self.__readers:
            if isinstance(reader, FileReader):
                items.append(reader.content)
                continue
            items.append(reader)
        return "\n".join(items)

class WebHookNamespace(dict):
    def __init__(self, name, *functions, **named_functions):
        self.name = name

        self.add_functions(*functions)
        self.add_named_functions(**named_functions)
    
    def add_functions(self, *functions):
        for function in functions:
            if getattr(function, "_module_api_class", False):
                self.add_functions(*function.functions)
                self.add_named_functions(**function.named_functions)
                continue
            
            if not inspect.isfunction(function) and not inspect.ismethod(function):
                raise TypeError(f"Expected a function for namespace, instead got '{type(function)}'")

            self.__setitem__(function.__name__, function)
    
    def add_named_functions(self, **functions):
        for funcname, function in functions.items():
            if not inspect.isfunction(function) and not inspect.ismethod(function):
                raise TypeError(f"Expected a function for namespace, instead got '{type(function)}'")

            self.__setitem__(funcname, function)
    
class WebHookFunction:
    def __new__(cls, function, window):
        def wrapper(*args, **kwargs):
            return function(window, *args, **kwargs)
        
        wrapper.__name__     = function.__name__
        wrapper.__qualname__ = function.__name__

        return wrapper

class WebHook:
    """
    A WebHook Object that contains information for handling a specific URL.

    :param url: The URL that the WebHook handles.
    :param html: A file or raw text of the HTML to render.
    :param css: A file path or list of file paths to style the HTML.
    :param functions: Functions to expose to JavaScript.
    :param namespaces: Namespaces to expose to JavaScript.
    :param homepage: If this WebHook is a homepage, it will be the fallback page if something goes wrong with the `Navigation` handler.
    :param encoding: The file encoding of the HTML and CSS files.

    :raises FileNotFoundWarning: Displays a warning if a file doesn't exist. (Only if warnings are enabled.)
    :raises FilePathLimitError: If a path exceeds the system limit for path lengths.
    """

    def __init__(self, url, html, css = None, functions = None, namespaces = None, homepage = False, encoding = "UTF-8"):
        self.url = _norm_url(url)
        self.css = css or ""
        self.html = html
        self.window = None
        self.elements = []
        self.homepage = homepage
        self.encoding = encoding
        self.functions = functions
        self.namespaces = namespaces

        self._get_html()
        self._get_css()
    
    def __repr__(self):
        return f"WebHook(url='{self.url}')"
    
    def _get_html(self):
        if not _check_exists(self.html): return
        self.html = FileReader(self.html, self.encoding).content
    
    def _get_css(self):
        if isinstance(self.css, (list, tuple, set,)):
            files = [item for item in self.css if _check_exists(item)]
            values = [item for item in self.css if not _check_exists(item)]
            self.css = "\n".join([CSSReader(*files, encoding=self.encoding).content, *values])
            return
        
        if isinstance(self.css, (str, bytes,)) and _check_exists(self.css):
            self.css = CSSReader(self.css, encoding=self.encoding).content
    
    def _wrap_functions(self):
        if self.window is None:
            return

        self.functions = [WebHookFunction(function, self.window) for function in self.functions]
    
    def _wrap_namespaces(self):
        if self.window is None:
            return
        
        for namespace in self.namespaces:
            for key in namespace.keys():
                namespace[key] = WebHookFunction(namespace[key], self.window)

    def set_window(self, window):
        """Sets the window of the WebHook."""
        self.window = window

class WebHookDict(dict):
    def __init__(self, webhooks):
        for webhook in webhooks:
            self[webhook.url] = webhook

    def __iter__(self):
        return self.items().__iter__

    def __repr__(self):
        return f"{{{', '.join([repr(webhook) for webhook in self.values()])}}}"
    
    def get(self, url):
        webhook = super().get(url, None)

        if webhook is None:
            raise WebHookNotFoundError(f"Failed to find WebHook for the url '{url}'")

        return webhook

def create_namespace(name, *functions, **named_functions):
    """
    Creates a `Namespace` to use within JavaScript.

    :param name: The alias the namespace is accessed by.
    :param functions: A list of functions to add.
    :param named_functions: A dictionary of functions to add.

    :returns: A `WebHookNamespace` object.

    The names of the regularly listed functions will be the value
    of the `__name__` property of the function objects.

    The names of the named function dictionary will be the keyword part.
    """

    return WebHookNamespace(name, *functions, **named_functions)