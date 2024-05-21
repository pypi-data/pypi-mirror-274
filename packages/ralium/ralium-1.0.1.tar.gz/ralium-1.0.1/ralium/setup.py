from PyInstaller.__main__ import logger, run as CompileExe
from ralium.errors import DisableWarnings, SetupError
from ralium.bundle import PyBundler
from ralium._util import __version__
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
    pyi_args = None
):
    """
    Compiles a Ralium project to an executable using PyInstaller.

    :param pyfile: Python file to compile.
    :param name: Display name for the executable.
    :param icon: Display icon for the executable.
    :param bundle: Bundles all of the html, css, python and image files into one executable. (Requires a `webfolder`)
    :param webfolder: Directory of the project.
    :param warnings: Calls the `DisableWarnings` to prevent warnings.
    :param onefile: Creates the executable as a standalone file.
    :param noconsole: Prevents a console from being displayed.
    :param bundle_dist: The directory name Ralium will use for bundling projects. (Default: `dist`)
    :param pyi_args: Extra parameters for PyInstaller to use.

    :raises TypeError: If the name or icon is not a `str` or `None`.
    :raises SetupError: If bundle is `True` while the webfolder is `None`.
    :raises RuntimeError: If this function is called within an already compiled executable file.
    :raises FileNotFoundError: If a certain file path doesn't exist.
    """

    logger.info("Ralium: %s", __version__)

    if bundle:
        if webfolder is None:
            raise SetupError("Cannot bundle project without a webfolder.")

        if bundle_dist is None:
            bundle_dist = "dist"
        
        bundle_dist = os.path.abspath(bundle_dist)

        if not os.path.exists(bundle_dist):
            os.mkdir(bundle_dist)
            logger.info("created %s", bundle_dist)

        name, ext = os.path.splitext(os.path.basename(pyfile))
        filename = os.path.join(bundle_dist, f"{name}.bundle{ext}")

        logger.info("Bundling '%s' with project '%s'", pyfile, os.path.abspath(webfolder))

        code = PyBundler(pyfile, webfolder).view()

        if not warnings:
            code.insert(0, b"import ralium.errors; ralium.errors.DisableWarnings()\n")

        with open(filename, "wb") as f:
            f.writelines(code)

        logger.info("wrote %s", filename)
        logger.info("Finished Bundling")

        pyfile = filename

    if getattr(sys, "frozen", False):
        raise RuntimeError("Ralium setup cannot be ran from an executable file.")
    
    if not os.path.exists(pyfile):
        raise FileNotFoundError(f"Failed to find python file '{pyfile}'")

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
    
    if webfolder and not bundle:
        for src, dst in collect_webfolder(webfolder).items():
            args.append(_add_data_arg(src, dst))

    CompileExe(args)