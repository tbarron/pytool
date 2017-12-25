import os
import py
import sys


# -----------------------------------------------------------------------------
def main():
    """
    Main entrypoint
    """
    print(sys.argv)
    print("produce skeletons for python programs")


# -----------------------------------------------------------------------------
def cfgdir():
    """
    This function's task is to return the path of the configuration dir. If env
    var PYTOOL_DIR is set, return its contents. Otherwise, if HOME is set,
    return HOME/.pytool. If neither PYTOOL_DIR nor HOME is set, raise
    FileNotFoundError

    If we return a path, we also return a second item indicating the source of
    the path, either 'env' if the config dir path was specified by env var
    PYTOOL_DIR or 'home' if the config dir path was taken from env var HOME +
    '.pytool'
    """
    trydir = os.getenv("PYTOOL_DIR")
    if trydir:
        return(trydir, "env")

    homedir = os.getenv("HOME")
    if homedir:
        ptdir = os.path.join(homedir, ".pytool")
        return(ptdir, "home")

    raise FileNotFoundError("Please set PYTOOL_DIR or HOME")


# -----------------------------------------------------------------------------
def ini_path():
    """
    The task for this function is to return the path of an existing pytool.ini
    file in the path returned by cfgdir(). If it does not exist, we raise a
    FileNotFoundError.
    """
    (cdir, _) = cfgdir()
    fpath = py.path.local(os.path.join(cdir, "pytool.ini"))
    if fpath.exists():
        return fpath.strpath
    else:
        msg = "No such file or directory: '{}'".format(fpath)
        raise FileNotFoundError(msg)


# -----------------------------------------------------------------------------
def initialize():
    """
    Find the path of pytool.ini if it exists
    """
    try:
        ptini = ini_path()
    except FileNotFoundError:
        setup_config_dir()

    ptini = ini_path()
    cfg = load_config(ptini)
    return cfg


# -----------------------------------------------------------------------------
def load_config(ptini):
    """
    Load the config info from cfgdir()/pytool.ini
    """
    pass


# -----------------------------------------------------------------------------
def setup_config_dir():
    """
    Create (if necessary) and populate the config dir
    """
    cdir, src = cfgdir()
    cdir = py.path.local(cdir)
    hdir = py.path.local(cdir.dirname)
    if src == "home" and not hdir.exists():
        raise FileNotFoundError("{} {}".format(hdir.strpath,
                                               "is not a directory"))

    try:
        cdir.ensure(dir=True)
    except py.error.EEXIST:
        msg = "{} is a file, cannot mkdir".format(cdir.strpath)
        raise FileExistsError(msg)

    ptini = cdir.join("pytool.ini")
    ptini.write([x + "\n"
                 for x in ["[pytool]",
                           "templates_dir = {}/{}".format(cdir.strpath,
                                                          "templates")]])

    tmpl = cdir.join("templates")  # .../templates
    tmpl.ensure(dir=True)

    pdir = tmpl.join("prjdir")    # .../templates/prjdir
    pdir.ensure(dir=True)

    ppdir = pdir.join("prjdir")   # .../templates/prjdir/prjdir
    ppdir.ensure(dir=True)

    tdir = pdir.join("test")      # .../templates/prjdir/test
    tdir.ensure(dir=True)

    prog = tmpl.join("prog.py")   # .../templates/prog.py
    prog.write(file_prog_py())

    tool = tmpl.join("tool.py")   # .../templates/tool.py
    tool.write(file_tool_py())

    init = ppdir.join("__init__.py")  # .../templates/prjdir/prjdir/__init__.py
    init.write(file_init_py())

    rdme = pdir.join("README.md")  # .../templates/prjdir/README.md
    rdme.write(file_readme())

    stup = pdir.join("setup.py")  # .../templates/prjdir/setup.py
    stup.write(file_setup_py())

    stub = tdir.join("test_stub.py")  # .../templates/prjdir/test/test_stub.py
    stub.write(file_test_stub_py())


# -----------------------------------------------------------------------------
def file_prog_py():
    """
    Return content for prog.py
    """
    pass


# -----------------------------------------------------------------------------
def file_tool_py():
    """
    Return content for tool.py
    """
    pass


# -----------------------------------------------------------------------------
def file_init_py():
    """
    Return content for __init__.py
    """
    pass


# -----------------------------------------------------------------------------
def file_readme():
    """
    Return content for README.md
    """
    pass


# -----------------------------------------------------------------------------
def file_setup_py():
    """
    Return content for setup.py
    """
    pass


# -----------------------------------------------------------------------------
def file_test_stub_py():
    """
    Return content for test_stub.py
    """
    pass


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
