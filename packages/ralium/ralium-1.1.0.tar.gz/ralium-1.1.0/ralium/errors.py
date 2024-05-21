import warnings

global __RALIUM_WARNING_MESSAGES__
__RALIUM_WARNING_MESSAGES__ = True

class SetupError(Exception): pass
class WindowLoadError(Exception): pass
class BridgeEventError(Exception): pass
class FilePathLimitError(Exception): pass
class RegistryNotFoundError(Exception): pass
class WindowNotRunningError(Exception): pass

class WebFunctionApiError(Exception): pass

class WebHookNotFoundError(Exception): pass
class WebHookHomepageError(Exception): pass

class WebFolderNotFoundError(Exception): pass
class WebRoutesNotFoundError(Exception): pass

class WebFolderDirectoryError(Exception): pass
class WebRoutesDirectoryError(Exception): pass

class FileNotFoundWarning(Warning): pass
class FilePathLimitWarning(Warning): pass

def DisableWarnings():
    """
    Disables Ralium warnings from being displayed.
    """

    global __RALIUM_WARNING_MESSAGES__
    __RALIUM_WARNING_MESSAGES__ = False

def warn(message, warning, major = False):
    return
    if not __RALIUM_WARNING_MESSAGES__:
        return

    if major:
        return warnings.warn(f"[Ralium]: {message}", warning)

    print(f"[Ralium] {warning.__name__}: {message}")