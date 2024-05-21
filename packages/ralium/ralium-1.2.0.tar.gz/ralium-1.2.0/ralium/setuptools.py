from PyInstaller.__main__ import logger, run as pack
from PyInstaller import compat

from ralium.errors import DisableWarnings, SetupError
from ralium.bundle import PyBundler
from ralium._util import __version__

import subprocess
import sys
import os

HTML_FILE_EXTENSIONS = [".htm", ".html"]
FILE_EXTENSIONS = [*HTML_FILE_EXTENSIONS, ".css", ".py"]

def _exe_str_error(name, var):
    return TypeError(f"Expected executable {name} to be of type 'str', instead got '{type(var)}'")

def _add_data_arg(src, dst):
    return f'--add-data={src}{os.pathsep}{dst}'

def collect_webfolder(webfolder):
    """
    Collects all necessary files from a Ralium Web Folder used within the executable main Python file.

    :param webfolder: The path to the project folder.
    
    :returns: A dictionary where the keys contain the absolute paths and the values represent the relative paths.
    """

    webfiles = {}
    webfolder = os.path.abspath(webfolder)
    webroutes = os.path.join(webfolder, "routes")
    cssfolder = os.path.join(webfolder, "styles")
    imgfolder = os.path.join(webfolder, "images")
    webfolder_name = os.path.basename(webfolder)
    
    if os.path.exists(webroutes):
        for root, _, files in os.walk(webroutes):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): dest for file in files if os.path.splitext(file)[-1] in FILE_EXTENSIONS})
    
    if os.path.exists(cssfolder):
        for root, _, files in os.walk(cssfolder):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): dest for file in files if os.path.splitext(file)[-1] == ".css"})
    
    if os.path.exists(imgfolder):
        for root, _, files in os.walk(imgfolder):
            dest = os.path.normpath(f"{webfolder_name}\\{root.removeprefix(webfolder)}")
            webfiles.update({os.path.join(root, file): dest for file in files})
    
    return webfiles

def bundle(
    pyfile,
    webfolder,
    name = None,
    warnings = False,
    distpath = None
):
    """
    Bundles a Ralium project to a single python file. Used for `webfolder` projects.

    :param pyfile: The python file to compile.
    :param webfolder: The path to the `webfolder`.
    :param name: The name of the file.
    :param warnings: Show warnings.
    :param distpath: The directory to create the bundle in. (Default: `dist`)
    
    :returns: The path to the bundled file created.

    :raises TypeError: If the incorrect types are provided for certain arguments.
    :raises SetupError: If the `webfolder` is `None`.
    :raises FileNotFoundError: If the `pyfile` or the `webfolder` path doesn't exist.
    """

    if webfolder is None:
        raise SetupError("Cannot bundle project without a webfolder.")

    distpath = os.path.abspath(distpath or "dist")

    if not os.path.exists(distpath):
        os.mkdir(distpath)
        logger.info("created %s", distpath)

    base, ext = os.path.splitext(os.path.basename(pyfile))
    filename = os.path.join(distpath, f"{name or base}.bundle{ext}")

    logger.info("Bundling '%s' with project '%s'", pyfile, os.path.abspath(webfolder))

    code = PyBundler(pyfile, webfolder).view()

    if not warnings:
        code.insert(0, b"import ralium.errors; ralium.errors.DisableWarnings()\n")
    
    # PyInstaller 6.6.0 and greater require these modules on Windows.
    # If you compile the program without these lines added to the file.
    # An ImportError will occur in which the pywin32-ctypes module needs to be installed.
    # Adding these lines as imports before everything else fixes this problem.
    if compat.is_win:
        code.insert(0, b"from win32ctypes.pywin32 import pywintypes\n")
        code.insert(1, b"from win32ctypes.pywin32 import win32api\n")

    with open(filename, "wb") as f:
        f.writelines(code)

    logger.info("wrote %s", filename)
    logger.info("Finished Bundling")

    return os.path.abspath(filename)

def setup(
    pyfile,
    name = None,
    icon = None,
    bundle = False,
    webfolder = None,
    warnings = False,
    onefile = True,
    noconsole = True,
    bundle_dist = None,
    pyi_args = None,
    use_subprocess = False,
    optimize_level = None
):
    """
    Compiles a Ralium project to an executable using PyInstaller.

    :param pyfile: The python file to compile.
    :param name: Display name for the executable.
    :param icon: Display icon for the executable.
    :param bundle: Bundles all of the html, css, python and image files into one executable. (Requires a `webfolder`)
    :param webfolder: Directory of the project.
    :param warnings: Calls the `DisableWarnings` to prevent warnings.
    :param onefile: Creates the executable as a standalone file.
    :param noconsole: Prevents a console from being displayed.
    :param bundle_dist: The directory name Ralium will use for bundling projects. (Default: `dist`)
    :param pyi_args: Extra parameters for PyInstaller to use.
    :param use_subprocess: Use `PyInstaller` through a subprocess.
    :param optimize_level: Set the `PYTHONOPTIMIZE` level. (Requires use_subprocess to be `True`)

    :raises TypeError: If the name or icon is not a `str` or `None`.
    :raises SetupError: If `bundle` is `True` while the `webfolder` is `None` or if `optimize_level` is set without `use_subprocess` being `True`.
    :raises RuntimeError: If this function is called within an already compiled executable file.
    :raises FileNotFoundError: If a certain file path doesn't exist.
    """

    logger.info("Ralium: %s", __version__)

    if getattr(sys, "frozen", False):
        raise RuntimeError("Ralium 'setup' cannot be ran from an executable file.")

    if not os.path.exists(pyfile):
        raise FileNotFoundError(f"Failed to find python file '{pyfile}'")
    
    if optimize_level is not None and not use_subprocess:
        raise SetupError("Optimization level can only be set if 'use_subprocess' is 'True'.")
    
    if optimize_level not in [None, *range(0, 3)]:
        raise ValueError("The optimization level must be in the range of 0 - 2.")

    args = [pyfile, *(pyi_args or [])]

    if name is not None:
        if not isinstance(name, str):
            raise _exe_str_error("name", name)
        
        args.append(f"--name={name}")
    
    if icon is not None:
        if not isinstance(icon, str):
            raise _exe_str_error("icon", icon)

        if not os.path.exists(icon):
            raise FileNotFoundError(f"Failed to find icon file with path: '{icon}'")
        
        args.append(f"--icon={icon}")
    
    if onefile:
        args.append(f"--onefile")
    
    if not warnings:
        DisableWarnings()
    
    if noconsole:
        args.append(f"--noconsole")
    
    if bundle:
        args[0] = globals()["bundle"](
            pyfile=pyfile, 
            webfolder=webfolder,
            name=name,
            warnings=warnings, 
            distpath=bundle_dist
        )
    elif webfolder:
        for src, dst in collect_webfolder(webfolder).items():
            args.append(_add_data_arg(src, dst))

    if use_subprocess:
        optimize_flag = ""

        match optimize_level:
            case 1: optimize_flag = "-O"
            case 2: optimize_flag = "-OO"
        
        args = [
            sys.executable,
            "-m",
            "PyInstaller",
            *args
        ]

        if optimize_flag:
            args.insert(1, optimize_flag)
        
        return subprocess.run(args) and None
    
    pack(args)