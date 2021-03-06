"""
pytool - produce skeletons for python programs

Usage:
    pytool help [COMMAND]
    pytool project [-d] PATH
    pytool program [-d] PATH
    pytool tool [-d] PATH
    pytool version [-d]

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
import configparser
from docopt_dispatch import dispatch
import os
import py
import pdb
from pytool.msgcat import mcat
from pytool import version


# -----------------------------------------------------------------------------
def main():
    """
    Main entrypoint
    """
    dispatch(__doc__)


# -----------------------------------------------------------------------------
@dispatch.on('help')
def pytool_help(**kwa):
    """
    With a trailing COMMAND value, provide more info about that command
    """
    if kwa['d']:
        pdb.set_trace()
    if 'program' == kwa['COMMAND']:
        print(mcat['hlpprogtxt'])
    elif 'project' == kwa['COMMAND']:
        print(mcat['hlpprojtxt'])
    elif 'tool' == kwa['COMMAND']:
        print(mcat['hlptooltxt'])
    else:
        if kwa['COMMAND']:
            print("{}: {}".format(mcat['unknown'], kwa['COMMAND']))
        print(__doc__)


# -----------------------------------------------------------------------------
@dispatch.on('project')
def make_project(**kwa):
    """
    Create a project directory
    """
    if kwa['d']:
        pdb.set_trace()
    create_project(kwa['PATH'])


# -----------------------------------------------------------------------------
@dispatch.on('program')
def make_program(**kwa):
    """
    Create a program file
    """
    if kwa['d']:
        pdb.set_trace()
    create_prog_tool(mcat['prog_py'], kwa['PATH'])


# -----------------------------------------------------------------------------
@dispatch.on('tool')
def make_tool(**kwa):
    """
    Create a tool
    """
    if kwa['d']:
        pdb.set_trace()
    create_prog_tool(mcat['tool_py'], kwa['PATH'])


# -----------------------------------------------------------------------------
def create_prog_tool(src, trg):
    """
    Create a program or tool
    """
    cfg = initialize()
    tmpldir = py.path.local(cfg.get(mcat['pytool'], 'templates_dir'))
    pysrc = tmpldir.join(src)
    pytrg = py.path.local(trg)
    pysrc.copy(pytrg)


# -----------------------------------------------------------------------------
def create_project(trgdir_s):
    """
    Create directory if it doesn't exist, then populate the template files
    """
    cfg = initialize()
    tmpldir = py.path.local(cfg.get(mcat['pytool'], 'templates_dir'))
    prjdir = tmpldir.join("prjdir")

    trgdir = py.path.local(trgdir_s)
    pdir = trgdir.join(trgdir.basename)

    for item in prjdir.visit(rec=True):
        relpath = item.strpath.replace(prjdir.strpath, "")
        trg = trgdir.join(relpath.replace('prjdir', pdir.basename))
        if item.isfile():
            py.path.local(trg.dirname).ensure(dir=True)
            item.copy(trg)
        elif item.isdir():
            trg.ensure(dir=True)


# -----------------------------------------------------------------------------
@dispatch.on('version')
def show_version(**kwa):
    """
    Report the current version
    """
    if kwa['d']:
        pdb.set_trace()
    print("pytool version {}".format(version.__version__))


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
def load_config(ptini=None):
    """
    Load the config info from cfgdir()/pytool.ini
    """
    if ptini is None:
        cdir, _ = cfgdir()
        ptpath = py.path.local(os.path.join(cdir, mcat['ptini']))
    else:
        ptpath = py.path.local(ptini)

    if ptpath.exists():
        rval = configparser.ConfigParser()
        rval.read(ptpath.strpath)
        return(rval)
    else:
        raise FileNotFoundError(ptpath.strpath)


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
        if not cdir.exists():
            print("{} '{}'".format(mcat['stupdir'], cdir.strpath))
            if src == mcat['lchome']:
                print(mcat['stupmv'])
        cdir.ensure(dir=True)
    except py.error.EEXIST:
        msg = "{} {}".format(cdir.strpath, mcat['isfile'])
        raise FileExistsError(msg)

    print("{} in {}".format(mcat['stupflz'], cdir.strpath))
    ptini = cdir.join(mcat['ptini'])
    ptini.write(file_pytool_ini())

    tmpl = cdir.join("templates")  # .../templates
    tmpl.ensure(dir=True)

    pdir = tmpl.join("prjdir")    # .../templates/prjdir
    pdir.ensure(dir=True)

    ppdir = pdir.join("prjdir")   # .../templates/prjdir/prjdir
    ppdir.ensure(dir=True)

    tdir = pdir.join("test")      # .../templates/prjdir/test
    tdir.ensure(dir=True)

    prog = tmpl.join(mcat["prog_py"])   # .../templates/prog.py
    prog.write(file_prog_py())

    tool = tmpl.join(mcat["tool_py"])   # .../templates/tool.py
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
def file_pytool_ini():
    """
    Return content for pytool.ini
    """
    cdir, _ = cfgdir()
    rval = "".join([x + mcat['newline'] for x in [
        mcat['sqpt'],
        "{}{} = {}/{}".format(mcat['tmpl'],
                              mcat['udir'],
                              cdir,
                              mcat['tmpl'])
        ]])
    return rval


# -----------------------------------------------------------------------------
def file_prog_py():
    """
    Return content for prog.py
    """
    rval = "".join([x + mcat['newline'] for x in [
        mcat['triquo'],
        mcat['descp'],
        mcat['triquo'],
        mcat['impsys'],
        mcat['empty'],
        mcat['empty'],
        mcat['divider'],
        mcat['defmn'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['mcom'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['prargs'],
        mcat['indent'] + mcat['where'],
        mcat['empty'],
        mcat['empty'],
        mcat['divider'],
        mcat['ifneqm'],
        mcat['indent'] + mcat['callmain'],
        ]])
    return rval


# -----------------------------------------------------------------------------
def file_tool_py():
    """
    Return content for tool.py
    """
    rval = "".join([x + "\n" for x in [
        mcat['triquo'],
        mcat['usage'],
        mcat['indent'] + mcat['cmdline'],
        mcat['empty'],
        mcat['options'],
        mcat['indent'] + mcat['debug'],
        mcat['triquo'],
        mcat['impdd'],
        mcat['impsys'],
        mcat['empty'],
        mcat['divider'],
        mcat['defmn'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['mcom'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['dispatch'],
        mcat['empty'],
        mcat['empty'],
        mcat['divider'],
        mcat['dispon'],
        mcat['deffunc'],
        mcat['indent'] + mcat['handle'],
        mcat['empty'],
        mcat['empty'],
        mcat['ifneqm'],
        mcat['indent'] + mcat['callmain'],
        ]])
    return rval


# -----------------------------------------------------------------------------
def file_init_py():
    """
    Return content for __init__.py
    """
    return file_prog_py()


# -----------------------------------------------------------------------------
def file_readme():
    """
    Return content for README.md
    """
    rval = "".join([x + "\n" for x in [
        mcat['title'],
        mcat['empty'],
        mcat['describe']
        ]])
    return rval


# -----------------------------------------------------------------------------
def file_setup_py():
    """
    Return content for setup.py
    """
    rval = "".join([x + "\n" for x in [
        mcat['impstp'],
        mcat['empty'],
        mcat['callstp'],
        mcat['indent'] + mcat['author'],
        mcat['indent'] + mcat['authmail'],
        mcat['indent'] + mcat['entpts'],
        mcat['indent'] + mcat['closep'],
        ]])
    return rval


# -----------------------------------------------------------------------------
def file_test_stub_py():
    """
    Return content for test_stub.py
    """
    rval = "".join([x + "\n" for x in [
        mcat['imppytst'],
        mcat['empty'],
        mcat['deftest'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['testdoc'],
        mcat['indent'] + mcat['triquo'],
        mcat['indent'] + mcat['writst'],
        ]])
    return rval


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
