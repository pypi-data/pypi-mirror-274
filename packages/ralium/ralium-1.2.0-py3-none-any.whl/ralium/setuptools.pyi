from ralium._util import (
    FilePathStr,
    DirPathStr,
    Any
)

HTML_FILE_EXTENSIONS: list[str]
FILE_EXTENSIONS: list[str]

def _exe_str_error(name: str, var: Any) -> Exception: ...
def _add_data_arg(src: FilePathStr, dst: FilePathStr) -> str: ...

def collect_webfolder(webfolder: DirPathStr) -> dict[FilePathStr]: ...

def bundle(
    pyfile: FilePathStr,
    webfolder: DirPathStr,
    name: str | None = None,
    warnings: bool = False,
    distpath: DirPathStr | None = None
) -> FilePathStr: ...

def setup(
    pyfile: FilePathStr,
    name: str | None = None,
    icon: FilePathStr | None = None,
    bundle: bool = False,
    webfolder: DirPathStr | None = None,
    warnings: bool = False,
    onefile: bool = True,
    noconsole: bool = True,
    bundle_dist: DirPathStr | None = None,
    pyi_args: list[str] | None = None,
    use_subprocess: bool = False,
    optimize_level: int | None = None
) -> None: ...