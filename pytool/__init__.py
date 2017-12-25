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
    """
    trydir = os.getenv("PYTOOL_DIR")
    if trydir:
        return(trydir)

    homedir = os.getenv("HOME")
    if homedir:
        ptdir = os.path.join(homedir, ".pytool")
        return(ptdir)

    raise FileNotFoundError("Please set PYTOOL_DIR or HOME")


# -----------------------------------------------------------------------------
def ini_path():
    """
    The task for this function is to return the path of an existing pytool.ini
    file in the path returned by cfgdir(). If it does not exist, we raise a
    FileNotFoundError.
    """
    cdir = cfgdir()
    fpath = py.path.local(os.path.join(cdir, "pytool.ini"))
    if fpath.exists():
        return fpath.strpath
    else:
        msg = "No such file or directory: '{}'".format(fpath)
        raise FileNotFoundError(msg)


if __name__ == "__main__":
    main()
