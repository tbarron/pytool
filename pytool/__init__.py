"""
pytool - produce skeletons for python programs

Usage:
    pytool help [COMMAND]
    pytool project [-d] PATH
    pytool program [-d] PATH
    pytool tool [-d] PATH

---
pytool examples:

    pytool help
        Display this list of command descriptions

    pytool project PATH
        Create a python project in PATH

    pytool program PATH
        Create a python program in PATH

    pytool tool PATH
        Create a new tool-style python program in PATH
---

Copyright (C) 1995 - <the end of time> Tom Barron
  tom.barron@comcast.net
  177 Crossroads Blvd
  Oak Ridge, TN  37830

This software is licensed under the CC-GNU GPL. For the full text of
the license, see http://creativecommons.org/licenses/GPL/2.0/

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import py
import pdb
from pytool.msgcat import mcat
from docopt_dispatch import dispatch


# -----------------------------------------------------------------------------
def main():
    """
    Main entrypoint
    """
    dispatch(__doc__)


# -----------------------------------------------------------------------------
@dispatch.on('tool')
def make_tool(**kwa):
    """
    Create a tool
    """
    if kwa['d']:
        pdb.set_trace()
    print(kwa)


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
    trydir = os.getenv(mcat['ptdir'])
    if trydir:
        return(trydir, mcat['env'])

    homedir = os.getenv(mcat['uchome'])
    if homedir:
        ptdir = os.path.join(homedir, mcat['dot_pt'])
        return(ptdir, mcat['lchome'])

    raise FileNotFoundError(mcat['please'])


# -----------------------------------------------------------------------------
def ini_path():
    """
    The task for this function is to return the path of an existing pytool.ini
    file in the path returned by cfgdir(). If it does not exist, we raise a
    FileNotFoundError.
    """
    (cdir, _) = cfgdir()
    fpath = py.path.local(os.path.join(cdir, mcat['ptini']))
    if fpath.exists():
        return fpath.strpath
    else:
        raise FileNotFoundError("{}: '{}'".format(mcat['nosuch'], fpath))


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
    if src == mcat['lchome'] and not hdir.exists():
        raise FileNotFoundError("{} {}".format(hdir.strpath, mcat['notdir']))

    try:
        cdir.ensure(dir=True)
    except py.error.EEXIST:
        msg = "{} {}".format(cdir.strpath, mcat['isfile'])
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
